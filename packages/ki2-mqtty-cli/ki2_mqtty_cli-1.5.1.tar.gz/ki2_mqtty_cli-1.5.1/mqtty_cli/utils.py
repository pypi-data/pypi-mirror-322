from __future__ import annotations
from typing import TYPE_CHECKING
from typing_extensions import Optional
import os
import argparse
from dataclasses import dataclass
from pathlib import Path

from .logging import getLogger

if TYPE_CHECKING:
    pass

logger = getLogger(__name__)


@dataclass
class CliArgs:
    config: Optional[str] = None
    threaded_device: Optional[int] = None


__parsed_args: CliArgs | None = None


def get_args():
    global __parsed_args

    if __parsed_args is not None:
        return __parsed_args

    parser = argparse.ArgumentParser(
        description="Command-line utility designed to facilitate the interconnection"
        " between serial devices and an MQTT server. This project is based on the"
        " `mqtty` library and allows simple configuration using a TOML file."
    )
    parser.add_argument("config", nargs="?", help="Path to config file")
    parser.add_argument(
        "--threaded-device",
        type=int,
        metavar="ID",
        help="Run device with given ID in a separate thread",
    )

    __parsed_args = CliArgs(**vars(parser.parse_args()))
    return __parsed_args


def get_path():
    configpath = get_args().config
    if configpath is not None:
        return Path(configpath)
    env_conf = os.getenv("MQTTY_CONFIG")
    if env_conf is not None:
        return Path(env_conf)
    return Path("settings.toml")
