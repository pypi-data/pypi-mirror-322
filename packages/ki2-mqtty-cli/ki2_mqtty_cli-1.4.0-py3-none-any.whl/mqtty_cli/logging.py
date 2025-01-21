from __future__ import annotations
from typing import TYPE_CHECKING
from typing_extensions import Optional
import logging
from pathlib import Path

from logging import getLogger as getLogger, Logger

if TYPE_CHECKING:
    from .config import LogLevel, DeviceConfig


def get_level(level: LogLevel | str | int = "info") -> int:
    if isinstance(level, int):
        return level
    if level == "debug":
        return logging.DEBUG
    elif level == "info":
        return logging.INFO
    elif level == "warning":
        return logging.WARNING
    elif level == "error":
        return logging.ERROR
    elif level == "critical":
        return logging.CRITICAL
    elif level == "notset":
        return logging.NOTSET
    else:
        raise ValueError(f"Unknown log level: {level}")


def set_logging_config(
    level: int | str = logging.INFO, *, logfile: Path | str | None = None
):
    logging.basicConfig(
        level=get_level(level),
        format="%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    if logfile is not None:
        logger = getLogger()
        fh = logging.FileHandler(logfile)
        fh.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        fh.setFormatter(formatter)
        logger.addHandler(fh)


def get_devie_formatter(device: DeviceConfig):
    device_name = device.name or device.port

    format = [
        "%(asctime)s.%(msecs)03d",
        "%(name)s",
        "%(levelname)s",
        device_name,
        "%(message)s",
    ]

    formatter = logging.Formatter(
        " - ".join(format),
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    return formatter


def configure_device_logger(device: DeviceConfig, logger: Optional[Logger] = None):
    logfile = device.logfile
    level = device.loglevel
    device_name = device.name or device.port

    format = [
        "%(asctime)s.%(msecs)03d",
        "%(name)s",
        "%(levelname)s",
        device_name,
        "%(message)s",
    ]

    formatter = logging.Formatter(
        " - ".join(format),
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    if logger is None:
        logger = getLogger()

    formatter = get_devie_formatter(device)

    for handler in logger.handlers:
        handler.setFormatter(formatter)

    if logfile is not None:
        fh = logging.FileHandler(logfile)
        fh.setLevel(get_level(level))
        fh.setFormatter(formatter)
        logger.addHandler(fh)


def get_device_logger(device_name: str):
    return logging.getLogger(device_name)
