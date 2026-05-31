"""
cli/logging_config.py
---------------------
Rotating-file logger shared by every CLI module.

Call `configure_logging()` once at startup (from `cli.main`). All modules
should use the stdlib pattern:

    import logging
    log = logging.getLogger(__name__)
"""
from __future__ import annotations

import logging
import logging.handlers
from pathlib import Path


def configure_logging(log_dir: Path, level: int = logging.DEBUG) -> None:
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "cli.log"

    fmt = logging.Formatter(
        fmt="%(asctime)s  %(levelname)-8s  %(name)-30s  %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )

    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=2 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(fmt)
    file_handler.setLevel(level)

    root = logging.getLogger()
    root.setLevel(level)
    root.addHandler(file_handler)

    # Silence noisy transport libraries unless we're debugging them.
    for noisy in ("httpx", "httpcore", "websockets", "asyncio", "urllib3"):
        logging.getLogger(noisy).setLevel(logging.WARNING)

    logging.getLogger("cli").setLevel(logging.DEBUG)
