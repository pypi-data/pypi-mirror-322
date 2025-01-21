from __future__ import annotations
from typing import TYPE_CHECKING
import asyncio


from .config import load_config
from .logging import set_logging_config, getLogger
from .utils import get_path, get_args

from .mode.simple import main_simple
from .mode.exp_multiprocess import main_experimental_multiprocess

if TYPE_CHECKING:
    pass

logger = getLogger(__name__)


def main():
    path = get_path()
    config = load_config(path)
    mode = config.running.mode
    loglevel = config.running.loglevel
    logfile = config.running.logfile

    set_logging_config(loglevel, logfile=logfile)

    logger.debug(f"Loaded config from {path}")
    logger.debug(f"Logging level set to {loglevel}")
    if logfile is not None:
        logger.debug(f"Logging to file {logfile}")

    logger.debug(f"Running in mode {mode}")
    threaded_device = get_args().threaded_device
    if threaded_device is not None:
        # TODO move at the correct place when implemented
        logger.debug(f"Running only device '{threaded_device}' in a separate thread")

    if mode.startswith("experimental"):
        logger.warning(f"Using experimental mode {config.running.mode}")

    if mode == "simple":
        asyncio.run(main_simple())
    elif mode == "experimental-multiprocess":
        main_experimental_multiprocess()
    else:
        raise ValueError(f"Unknown mode {config.running.mode}")


if __name__ == "__main__":
    main()
