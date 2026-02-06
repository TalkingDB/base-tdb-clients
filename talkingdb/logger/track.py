import time
import inspect
import traceback
from functools import wraps
from typing import Callable

from ..logger.context import get_log_context
from ..logger.file import file_log


def _resolve_function(func: Callable, resolve_from: str = None) -> str:
    if resolve_from:
        return resolve_from.split(".")[-1]
    return func.__name__


def _resolve_module(func: Callable, resolve_from: str = None) -> str:
    if resolve_from:
        return resolve_from
    return f"{func.__module__}.{func.__name__}"


def _resolve_client(func: Callable, resolve_from: str = None) -> str:
    if resolve_from:
        parts = resolve_from.split(".")
    else:
        parts = func.__module__.split(".")

    if parts and parts[0] == "talkingdb":
        return parts[2] if len(parts) > 2 else "unknown"

    return parts[-2] if len(parts) >= 2 else "unknown"


def track(
    resolve_from: str | None = None,
    *,
    log_response: bool = False,
    response_key: str = None,
    response_serializer: Callable | None = None,
):
    def decorator(func: Callable):

        function_name = _resolve_function(func, resolve_from)
        module_name = _resolve_module(func, resolve_from)
        client_name = _resolve_client(func, resolve_from)

        is_async = inspect.iscoroutinefunction(func)

        def _serialize_response(result):
            if response_serializer:
                try:
                    return response_serializer(result)
                except Exception:
                    return "<response_serialization_failed>"
            try:
                return result if isinstance(result, (dict, list, str, int, float, bool)) else str(result)
            except Exception:
                return "<unserializable_response>"

        def _build_entry(
            *,
            status: str,
            duration_ms: int,
            result=None,
            error_tb: str | None = None,
        ):
            entry = {
                "client": client_name,
                "function": function_name,
                "module": module_name,
                "status": status,
                "duration_ms": duration_ms,
                **get_log_context(),
            }

            if error_tb:
                entry["traceback"] = error_tb

            if (
                log_response
                and status == "success"
                and result is not None
                and entry.get("scope")
                and entry.get("event_group_id")
                and entry.get("service")
            ):
                entry["response_key"] = response_key
                entry["response"] = _serialize_response(result)
                entry["_scoped_flat"] = True

            return entry

        if is_async:

            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                start = time.perf_counter()
                try:
                    result = await func(*args, **kwargs)
                    duration_ms = int((time.perf_counter() - start) * 1000)

                    file_log(
                        _build_entry(
                            status="success",
                            duration_ms=duration_ms,
                            result=result,
                        )
                    )
                    return result

                except Exception:
                    duration_ms = int((time.perf_counter() - start) * 1000)

                    file_log(
                        _build_entry(
                            status="error",
                            duration_ms=duration_ms,
                            error_tb=traceback.format_exc(),
                        )
                    )
                    raise

            return async_wrapper

        else:

            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                start = time.perf_counter()
                try:
                    result = func(*args, **kwargs)
                    duration_ms = int((time.perf_counter() - start) * 1000)

                    file_log(
                        _build_entry(
                            status="success",
                            duration_ms=duration_ms,
                            result=result,
                        )
                    )
                    return result

                except Exception:
                    duration_ms = int((time.perf_counter() - start) * 1000)

                    file_log(
                        _build_entry(
                            status="error",
                            duration_ms=duration_ms,
                            error_tb=traceback.format_exc(),
                        )
                    )
                    raise

            return sync_wrapper

    return decorator
