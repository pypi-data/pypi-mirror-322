from __future__ import annotations
from typing import TYPE_CHECKING
from typing_extensions import Any
import multiprocessing
import asyncio
import os

from aiomqtt import Client as AioMqttClient
from ki2_python_utils import run_parallel
from mqtty import serial_device_factory, manager_setup, connect_aio_mqtt, MqttyDevice

from mqtty_cli.config import get_config, convert_parity
from mqtty_cli.logging import getLogger, configure_device_logger
from mqtty_cli.sync_to_async import (
    ask_publish_sync,
    handle_queue,
    change_mqtt_connexion_status,
)
from mqtty_cli.cli import get_args

if TYPE_CHECKING:
    pass

logger = getLogger(__name__)


def publish_notif(payload: dict[str, Any]):
    notification_topic = get_config().mqtt.notification_topic
    if notification_topic is None:
        return
    ask_publish_sync(notification_topic, payload)


def on_serial_error(device: MqttyDevice, error: Exception):
    logger.error(f"Error occured on device {device.name}: {error}")

    publish_notif(
        {
            "type": "exception",
            "source": "serial",
            "device": device.name,
            "message": str(error),
        }
    )


async def main_device(id: int):
    config = get_config()

    mqtt_config: dict[str, Any] = {
        "hostname": config.mqtt.host,
        "port": config.mqtt.port,
    }

    if config.mqtt.auth is not None:
        mqtt_config["username"] = config.mqtt.auth.username
        mqtt_config["password"] = config.mqtt.auth.password

    if config.mqtt.auth is not None:
        mqtt_config["username"] = config.mqtt.auth.username
        mqtt_config["password"] = config.mqtt.auth.password

    if config.mqtt.startup_wait_time > 0:
        await asyncio.sleep(config.mqtt.startup_wait_time)

    mqtt_client = AioMqttClient(**mqtt_config)

    if (
        isinstance(config.mqtt.pending_calls_threshold, int)
        and config.mqtt.pending_calls_threshold > 0
    ):
        mqtt_client.pending_calls_threshold = config.mqtt.pending_calls_threshold

    manager = manager_setup("async")
    manager.on_serial_error = on_serial_error

    device = config.devices[id]

    topic = device.topic
    optional = device.optional
    serial_config = device.model_dump(
        exclude={"topic", "optional", "logfile", "loglevel"}
    )
    if optional:
        if not os.path.exists(device.port):
            msg = f"Optional device '{device.port}' not found - skipping"
            logger.warning(msg)
            publish_notif(
                {
                    "type": "info",
                    "source": "setup",
                    "message": msg,
                    "device": device.name,
                    "status": "not-found",
                }
            )
            return
    if serial_config["baudrate"] is None:
        serial_config["baudrate"] = config.default.baudrate
    serial_config["parity"] = convert_parity(serial_config["parity"])
    serial_device = serial_device_factory(**serial_config)
    manager.register(topic, serial_device)
    msg = f"New device '{device.port}' on topic '{topic}'"
    logger.info(msg)
    publish_notif(
        {
            "type": "info",
            "source": "setup",
            "message": msg,
            "device": device.name,
            "status": "connected",
        }
    )

    mqtt_loop = connect_aio_mqtt(
        mqtt_client, manager=manager, conn_cb=change_mqtt_connexion_status
    )

    async def _handle_queue():
        await handle_queue(mqtt_client)

    await run_parallel(manager.loop, mqtt_loop, _handle_queue)


def run_device_process(device_id: int):
    """
    Function executed by each process to handle a specific device.

    Args:
        device_id (int): The ID of the device to be managed by this process.
    """
    config = get_config()
    device = config.devices[device_id]
    configure_device_logger(device)
    try:
        logger.info(f"Process started for device ID {device_id}")
        asyncio.run(main_device(device_id))
    except Exception as e:
        logger.error(f"Error in process for device ID {device_id}: {e}")


def main_experimental_multiprocess():
    """
    Main entry point for the experimental multiprocessing mode.
    Depending on the command-line arguments, it will either:
    - Run a single device process if a specific device ID is provided.
    - Spawn separate processes for all devices if no specific device ID is provided.
    """
    config = get_config()
    args = get_args()

    if args.threaded_device is not None:
        # Launch a single device (existing behavior)
        id = args.threaded_device
        if id < 0 or id >= len(config.devices):
            logger.error(f"Invalid device ID {id}")
            return
        asyncio.run(main_device(id))
        return

    # Launch all devices in separate processes
    logger.info("Launching all devices in separate processes...")
    processes: list[multiprocessing.Process] = []

    for id in range(len(config.devices)):
        p = multiprocessing.Process(target=run_device_process, args=(id,))
        processes.append(p)
        p.start()
        logger.info(f"Launched process for device ID {id}")

    # Wait for all processes to finish
    for p in processes:
        p.join()
