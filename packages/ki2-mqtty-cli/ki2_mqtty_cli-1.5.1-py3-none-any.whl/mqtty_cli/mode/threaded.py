from __future__ import annotations
from typing import TYPE_CHECKING
import time
import os

import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
from mqtty import serial_device_factory, manager_setup, connect_paho_mqtt, MqttyDevice

from mqtty_cli.config import get_config, convert_parity
from mqtty_cli.logging import getLogger

if TYPE_CHECKING:
    pass

logger = getLogger(__name__)


def on_serial_error(device: MqttyDevice, error: Exception):
    logger.error(f"Error occured on device {device.name}: {error}")


def on_mqtt_message(topic: str, message: str):
    logger.debug(f"{topic} - {message}")


def main_experimental_threaded():
    config = get_config()

    if len(config.devices) == 0:
        logger.warning("No devices configured")
        return

    if config.mqtt.startup_wait_time > 0:
        time.sleep(config.mqtt.startup_wait_time)

    mqtt_client = mqtt.Client(CallbackAPIVersion.VERSION2)
    if config.mqtt.auth is not None:
        mqtt_client.username_pw_set(
            config.mqtt.auth.username, config.mqtt.auth.password
        )

    manager = manager_setup("threaded")
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
                continue
        if serial_config["baudrate"] is None:
            serial_config["baudrate"] = config.default.baudrate
        serial_config["parity"] = convert_parity(serial_config["parity"])
        serial_device = serial_device_factory(**serial_config)
        manager.register(topic, serial_device)
        msg = f"New device '{device.port}' on topic '{topic}'"
        logger.info(msg)

    connect_paho_mqtt(mqtt_client, manager=manager, callback=on_mqtt_message)

    manager.start()
    mqtt_client.connect(config.mqtt.host, config.mqtt.port, 60)
    mqtt_client.loop_forever(retry_first_connection=True)
