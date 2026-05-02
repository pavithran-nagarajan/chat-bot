import os
import logging
import logging.config
import logging.handlers
import sys
from datetime import datetime
from pathlib import Path


# ---------------------------------------------------------------------------
# Level-exact filter
# ---------------------------------------------------------------------------

class MinLevelFilter(logging.Filter):
    """Only allow logs at EXACTLY this level — not above."""
    def __init__(self, level: int):
        self.level = level

    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno == self.level


# ---------------------------------------------------------------------------
# Daily handler — filenames like debug_20260502.log
# ---------------------------------------------------------------------------

class DailyNamedFileHandler(logging.handlers.TimedRotatingFileHandler):
    """
    Rotates at midnight and names files as:
        <level>_YYYYMMDD.log
    e.g. debug_20260502.log, error_20260503.log
    """

    def __init__(self, base_dir: str, level_name: str, **kwargs):
        self.base_dir  = base_dir
        self.level_name = level_name
        filename = self._today_path()
        super().__init__(
            filename,
            when="midnight",
            interval=1,
            **kwargs,
        )
        # Override the suffix/namer so rotated files also follow YYYYMMDD
        self.suffix = "%Y%m%d"
        self.namer  = self._namer

    # ------------------------------------------------------------------
    def _today_path(self) -> str:
        date_str = datetime.now().strftime("%Y%m%d")
        return os.path.join(
            self.base_dir,
            self.level_name,
            f"{self.level_name}_{date_str}.log",
        )

    def _namer(self, default_name: str) -> str:
        """
        TimedRotatingFileHandler passes:
            /path/level_20260502.log.20260503
        We want:
            /path/level_20260503.log
        """
        date_part = default_name.rsplit(".", 1)[-1]   # "20260503"
        return os.path.join(
            self.base_dir,
            self.level_name,
            f"{self.level_name}_{date_part}.log",
        )

    # Keep the base filename in sync after each rotation
    def doRollover(self) -> None:
        super().doRollover()
        self.baseFilename = os.path.abspath(self._today_path())


# ---------------------------------------------------------------------------
# Logging config dict  (filenames / base_dir patched at startup)
# ---------------------------------------------------------------------------

LOGGING_CONFIG: dict = {
    "version": 1,
    "disable_existing_loggers": False,

    # ── Filters ─────────────────────────────────────────────────────────────
    "filters": {
        "debug_only":    {"()": MinLevelFilter, "level": logging.DEBUG},
        "info_only":     {"()": MinLevelFilter, "level": logging.INFO},
        "warning_only":  {"()": MinLevelFilter, "level": logging.WARNING},
        "error_only":    {"()": MinLevelFilter, "level": logging.ERROR},
        "critical_only": {"()": MinLevelFilter, "level": logging.CRITICAL},
    },

    # ── Formatters ──────────────────────────────────────────────────────────
    "formatters": {
        "console": {
            "format":  "%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s",
            "datefmt": "%H:%M:%S",
        },
        "file": {
            "format":  "%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },

    # ── Handlers ────────────────────────────────────────────────────────────
    "handlers": {
        # Console — all levels
        "console": {
            "class":     "logging.StreamHandler",
            "formatter": "console",
            "level":     "DEBUG",
            "stream":    "ext://sys.stdout",
        },

        # File handlers — one per level, daily rotation, YYYYMMDD filenames
        # base_dir is overwritten by setup_logging() using UPLOAD_PATH env var
        "file_debug": {
            "()":          DailyNamedFileHandler,
            "base_dir":    "upload/logs",       # overwritten at startup
            "level_name":  "debug",
            "backupCount": 30,
            "level":       "DEBUG",
            "filters":     ["debug_only"],
            "encoding":    "utf-8",
            "formatter":   "file",
        },
        "file_info": {
            "()":          DailyNamedFileHandler,
            "base_dir":    "upload/logs",
            "level_name":  "info",
            "backupCount": 30,
            "level":       "INFO",
            "filters":     ["info_only"],
            "encoding":    "utf-8",
            "formatter":   "file",
        },
        "file_warning": {
            "()":          DailyNamedFileHandler,
            "base_dir":    "upload/logs",
            "level_name":  "warning",
            "backupCount": 30,
            "level":       "WARNING",
            "filters":     ["warning_only"],
            "encoding":    "utf-8",
            "formatter":   "file",
        },
        "file_error": {
            "()":          DailyNamedFileHandler,
            "base_dir":    "upload/logs",
            "level_name":  "error",
            "backupCount": 30,
            "level":       "ERROR",
            "filters":     ["error_only"],
            "encoding":    "utf-8",
            "formatter":   "file",
        },
        "file_critical": {
            "()":          DailyNamedFileHandler,
            "base_dir":    "upload/logs",
            "level_name":  "critical",
            "backupCount": 30,
            "level":       "CRITICAL",
            "filters":     ["critical_only"],
            "encoding":    "utf-8",
            "formatter":   "file",
        },
    },

    # ── Root logger ─────────────────────────────────────────────────────────
    "root": {
        "level": "DEBUG",
        "handlers": [
            "console",
            "file_debug",
            "file_info",
            "file_warning",
            "file_error",
            "file_critical",
        ],
    },
}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def setup_logging() -> None:
    """Call once at application startup."""
    strUploadPath = os.getenv("UPLOAD_PATH", "uploads")
    log_base = strUploadPath + "/logs"

    # Create per-level subdirectories
    for level in ("debug", "info", "warning", "error", "critical"):
        Path(log_base + "/" + level).mkdir(parents=True, exist_ok=True)
        # Patch base_dir so DailyNamedFileHandler writes to the correct path
        LOGGING_CONFIG["handlers"][f"file_{level}"]["base_dir"] = log_base

    logging.config.dictConfig(LOGGING_CONFIG)
    _install_global_exception_handler(logging.getLogger())


def get_logger(name: str) -> logging.Logger:
    """Get a named logger.  Pass __name__ from the calling module."""
    return logging.getLogger(name)


# ---------------------------------------------------------------------------
# Unhandled-exception hook
# ---------------------------------------------------------------------------

def _install_global_exception_handler(logger: logging.Logger) -> None:
    def handle_exception(exc_type, exc_value, exc_tb):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_tb)
            return
        logger.critical(
            "Unhandled exception",
            exc_info=(exc_type, exc_value, exc_tb),
        )

    sys.excepthook = handle_exception