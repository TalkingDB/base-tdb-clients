import os
import sqlite3
import threading
from contextlib import contextmanager

GRAPH_DB = os.getenv("GRAPH_DB", "data/graphs.db")

_thread_local = threading.local()


def _ensure_db_path():
    db_dir = os.path.dirname(GRAPH_DB)
    if db_dir:  # handles case where only filename is given
        os.makedirs(db_dir, exist_ok=True)


def _create_connection() -> sqlite3.Connection:
    _ensure_db_path()  # 👈 ensure folder exists

    conn = sqlite3.connect(
        GRAPH_DB,
        check_same_thread=False,
        isolation_level=None
    )

    conn.row_factory = sqlite3.Row

    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    conn.execute("PRAGMA temp_store=MEMORY;")

    return conn


def get_connection() -> sqlite3.Connection:
    conn = getattr(_thread_local, "conn", None)
    if conn is None:
        conn = _create_connection()
        _thread_local.conn = conn
    return conn


@contextmanager
def sqlite_conn():
    conn = get_connection()
    try:
        yield conn
    finally:
        pass