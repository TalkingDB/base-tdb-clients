# Troubleshooting

[Docs home](README.md) › Troubleshooting

| Symptom | Likely cause | Fix |
| :--- | :--- | :--- |
| `sqlite3.OperationalError: database is locked` | Another writer held the lock longer than the busy timeout | Raise `TDB_SQLITE_BUSY_TIMEOUT_MS`, keep write transactions short, and avoid sharing one database file between processes that write heavily |
| Changing `ENTITY_DB` (or another path) in code has no effect | The value is read when the module is first imported | Set the environment variable before the process starts, or before the first `import talkingdb...` |
| `RuntimeError: MinIO is not configured.` | `get_minio_client()` was called without `MINIO_ACCESS_KEY` and `MINIO_SECRET_KEY` | Set both keys, or check `is_configured()` first and skip storage |
| Startup warning: [MinIO](https://en.wikipedia.org/wiki/MinIO) storage is disabled | Normal when MinIO keys are not set | Nothing to fix unless you need file storage |
| A temporary database folder cannot be deleted on Windows | Cached connections are never closed by this library, so Windows keeps the files locked | Delete at process exit on a best effort basis, or close the connection yourself before deleting |
| `logs/talkingdb/` keeps growing | `@track()` appends a line for every call, in at least two files | Rotate or delete old `.jsonl` files on a schedule; the folder is relative to the working directory |
| Data written in one thread is not visible in another straight away | Each thread has its own connection; WAL readers see the last committed state | Make sure the writer commits; with autocommit this happens per statement unless you opened a `BEGIN` |

## Further reading

- [SQLite: database is locked, explained](https://www.sqlite.org/rescode.html#busy)
- [SQLite write ahead logging](https://www.sqlite.org/wal.html)

---

**Related:** [Architecture](architecture.md) · [Usage and examples](usage-and-examples.md) · [README](../README.md)
