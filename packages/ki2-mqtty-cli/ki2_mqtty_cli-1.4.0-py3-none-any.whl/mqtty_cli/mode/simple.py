from __future__ import annotations
from typing import TYPE_CHECKING
from typing_extensions import Any
import asyncio
import os

from aiomqtt import Client as AioMqttClient
from ki2_python_utils import run_parallel
from mqtty import serial_device_factory, manager_setup, connect_aio_mqtt, MqttyDevice

from mqtty_cli.config import get_config, convert_parity
from mqtty_cli.logging import getLogger
from mqtty_cli.sync_to_async import (
    ask_publish_sync,
    handle_queue,
    change_mqtt_connexion_status,
)

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


async def main_simple():
    config = get_config()

    if len(config.devices) == 0:
        logger.warning("No devices configured")
        return

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

    for device in config.devices:
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
                continue
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
