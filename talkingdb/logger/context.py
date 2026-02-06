from contextvars import ContextVar
from typing import Dict, Any

_log_context: ContextVar[Dict[str, Any]] = ContextVar(
    "log_context",
    default={},
)

_tracker_context: ContextVar[Dict[str, Any]] = ContextVar(
    "tracker_context",
    default={},
)


# ---------- Log Context (business) ----------

def set_log_context(**kwargs):
    ctx = _log_context.get().copy()
    ctx.update(kwargs)
    _log_context.set(ctx)


def get_log_context() -> Dict[str, Any]:
    return _log_context.get()


def clear_log_context():
    _log_context.set({})


# ---------- Tracker Context (execution) ----------

def set_tracker_context(**kwargs):
    ctx = _tracker_context.get().copy()
    ctx.update(kwargs)
    _tracker_context.set(ctx)


def get_tracker_context() -> Dict[str, Any]:
    return _tracker_context.get()


def clear_tracker_context():
    _tracker_context.set({})
