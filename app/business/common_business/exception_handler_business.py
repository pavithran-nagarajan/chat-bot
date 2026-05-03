from app.business.common_business.logging_business import get_logger
from fastapi import HTTPException

logger = get_logger(__name__)


def handle_exception(e: Exception, context: str = "") -> None:
    exception_map = {
        # (log_fn, label, http_status_code)
        ValueError:         (_log_warning,  "ValueError",         400),
        TypeError:          (_log_warning,  "TypeError",          400),
        AttributeError:     (_log_warning,  "AttributeError",     400),
        KeyError:           (_log_warning,  "KeyError",           400),
        IndexError:         (_log_warning,  "IndexError",         400),
        ZeroDivisionError:  (_log_warning,  "ZeroDivisionError",  400),
        FileNotFoundError:  (_log_error,    "FileNotFoundError",  404),
        PermissionError:    (_log_error,    "PermissionError",    403),
        TimeoutError:       (_log_error,    "TimeoutError",       408),
        ConnectionError:    (_log_error,    "ConnectionError",    503),
        IOError:            (_log_error,    "IOError",            500),
        OSError:            (_log_error,    "OSError",            500),
        RuntimeError:       (_log_error,    "RuntimeError",       500),
        RecursionError:     (_log_error,    "RecursionError",     500),
        OverflowError:      (_log_error,    "OverflowError",      500),
        MemoryError:        (_log_critical, "MemoryError",        500),
    }

    # Match exception type
    for exc_type, (log_fn, label, status_code) in exception_map.items():
        if isinstance(e, exc_type):
            log_fn(label, context, e)
            raise HTTPException(
                status_code=status_code,
                detail=f"{label}: {str(e)}"
            )

    # Fallback — unhandled exception
    _log_critical("Unhandled Exception", context, e)
    raise HTTPException(
        status_code=500,
        detail=f"Unexpected error: {str(e)}"
    )


# ─── Log Helpers ──────────────────────────────────────────────────────────────

def _log_warning(label: str, context: str, e: Exception) -> None:
    logger.warning(f"{label} | {context} | {str(e)}")

def _log_error(label: str, context: str, e: Exception) -> None:
    logger.error(f"{label} | {context} | {str(e)}")

def _log_critical(label: str, context: str, e: Exception) -> None:
    logger.critical(f"{label} | {context} | {str(e)}", exc_info=e)
