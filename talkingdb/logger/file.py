import json
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

LOG_ROOT = Path("logs/talkingdb")


def _ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def _write_jsonl(path: Path, payload: Dict[str, Any], indent=None):
    _ensure_dir(path.parent)
    with path.open("a") as f:
        f.write(json.dumps(payload, default=str, indent=indent) + "\n")


def file_log(entry: Dict[str, Any]):
    status = entry.get("status", "unknown")
    client = entry.get("client", "unknown")
    function = entry.get("function", "unknown")
    service = entry.get("service")
    scope = entry.get("scope")
    event_group_id = entry.get("event_group_id")

    entry = dict(entry)
    entry.setdefault("timestamp", datetime.utcnow().isoformat())

    _indent = None
    is_flat = entry.pop("_scoped_flat", False)
    response_key = entry.pop("response_key", None)

    # ---------- Group 1 ----------
    # /[client]/[success|error]/function.jsonl
    if not is_flat:
        g1_path = (
            LOG_ROOT
            / client
            / status
            / f"{function}.jsonl"
        )
        _write_jsonl(g1_path, entry)

    # ---------- Group 2 ----------
    # scoped logging (supports flattened service-only paths)
    if scope and event_group_id and service:

        if is_flat:
            # /[scope]/[event_group_id]/[service]/function.jsonl
            g2_path = (
                LOG_ROOT
                / scope
                / event_group_id
                / service
                / f"{response_key}.json" if response_key else f"{function}.jsonl"
            )
            _indent = 2 if response_key else None
        else:
            # /[scope]/[event_group_id]/[service]/[client]/[success|error]/function.jsonl
            g2_path = (
                LOG_ROOT
                / scope
                / event_group_id
                / service
                / client
                / status
                / f"{function}.jsonl"
            )

        _write_jsonl(g2_path, entry, _indent)

    # ---------- Group 3 ----------
    # /success.jsonl or /error.jsonl
    g3_path = LOG_ROOT / f"{status}.jsonl"
    _write_jsonl(g3_path, entry)
