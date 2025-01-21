from __future__ import annotations
from typing import TYPE_CHECKING, cast
from typing_extensions import Optional, Annotated, Literal, TypeAlias
from pathlib import Path

import tomli
from pydantic import BaseModel, AfterValidator

if TYPE_CHECKING:
    pass


ParityFullType: TypeAlias = Literal["None", "Even", "Odd", "Mark", "Space"]
ParityLimitedType: TypeAlias = Literal["N", "E", "O", "M", "S"]
ParityType: TypeAlias = ParityFullType | ParityLimitedType


ExperimentalRunningMode: TypeAlias = Literal["experimental-multiprocess"]
RunningMode: TypeAlias = Literal["simple"] | ExperimentalRunningMode
LogLevel: TypeAlias = Literal["debug", "info", "warning", "error", "critical", "notset"]


def convert_parity(value: ParityType) -> ParityLimitedType:
    if len(value) > 0:
        value = cast(ParityLimitedType, value[0])
    return cast(ParityLimitedType, value)


class RunningConfig(BaseModel):
    logfile: Optional[str] = None
    mode: RunningMode = "simple"
    loglevel: LogLevel = "info"


class MqttAuthConfig(BaseModel):
    username: str
    password: str


class MqttConfig(BaseModel):
    host: str = "localhost"
    port: int = 1883
    auth: Optional[MqttAuthConfig] = None
    notification_topic: Optional[str] = None
    startup_wait_time: int | float = 0  # seconds (to wait for mqtt broker to start)
    pending_calls_threshold: Optional[int] = None


def one_char_string(value: str) -> str:
    if len(value) != 1:
        raise ValueError("Must be a single character")
    return value


class DefaultConfig(BaseModel):
    baudrate: int = 9600


class DeviceConfig(BaseModel):
    topic: str
    port: str
    name: Optional[str] = None
    optional: Optional[bool] = True
    logfile: Optional[str] = None
    loglevel: LogLevel = "info"
    baudrate: Optional[int] = None
    bytesize: int = 8
    parity: ParityType = "None"
    stopbits: float = 1
    timeout: Optional[int] = None
    xonxoff: bool = False
    rtscts: bool = False
    write_timeout: Optional[float] = None
    dsrdtr: bool = False
    inter_byte_timeout: Optional[float] = None
    exclusive: Optional[bool] = None
    endline_char: Annotated[str, AfterValidator(one_char_string)] = "\n"
    mqtt_start: Annotated[str, AfterValidator(one_char_string)] = "@"
    mqtt_separator: Annotated[str, AfterValidator(one_char_string)] = ":"
    log_non_mqtt_message: bool = True


class TomlConfig(BaseModel):
    running: RunningConfig = RunningConfig()
    mqtt: MqttConfig = MqttConfig()
    default: DefaultConfig = DefaultConfig()
    devices: list[DeviceConfig] = []


__global_config: Optional[TomlConfig] = None


def load_config(path: str | Path) -> TomlConfig:
    global __global_config
    if __global_config is not None:
        raise ValueError("Configuration already loaded")

    with open(path, "rb") as f:
        data = tomli.load(f)

    __global_config = TomlConfig(**data)
    return __global_config


def get_config() -> TomlConfig:
    global __global_config
    if __global_config is None:
        raise ValueError("Configuration not loaded")
    return __global_config
