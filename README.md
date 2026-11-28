<!-- short-readme -->
<h1 align="center">base-tdb-clients</h1>

<p align="center"><b>Shared connections to SQLite, MinIO and logs for TalkingDB services.</b></p>

<p align="center"><a href="#try-it">Try it</a> · <a href="docs/architecture.md">How it works</a> · <a href="docs/usage-and-examples.md">Usage and examples</a> · <a href="docs/troubleshooting.md">Troubleshooting</a> · <a href="docs/reference.md">Full reference</a></p>

<p align="center"><a href="https://github.com/TalkingDB/base-tdb-clients/stargazers"><img src="https://img.shields.io/github/stars/TalkingDB/base-tdb-clients?style=social" alt="GitHub stars"></a> <a href="https://www.gnu.org/licenses/agpl-3.0.html"><img src="https://img.shields.io/badge/license-AGPL--3.0-blue" alt="AGPL-3.0"></a></p>

<p align="center">
  <img src="docs/images/demo.gif" alt="Animated demo of a real run: each thread gets its own cached SQLite connection in WAL mode with a 30 second busy timeout, the -wal and -shm files appear on disk, and @track files successes and errors per client and function">
</p>
<p align="center"><sub>A real run at <code>a60b646</code> with Python 3.13.18, 26 Nov 2026.</sub></p>

One place to open [SQLite](https://www.sqlite.org/about.html) databases (one cached connection per thread, [WAL mode](https://www.sqlite.org/wal.html), a 30 second busy timeout), talk to [MinIO](https://en.wikipedia.org/wiki/MinIO) file storage, and write structured call logs.

## What it does

- **SQLite**: `get_connection(path)` gives each thread its own cached connection ([usage](docs/usage-and-examples.md)).
- **MinIO**: object storage, only when configured.
- **Logging**: `@track` files every call's success or error as JSON lines ([how it works](docs/architecture.md)).

## Try it

```bash
git clone https://github.com/TalkingDB/base-tdb-clients.git
cd base-tdb-clients
poetry install
```

Then open a database: `get_connection('data/demo.db')` prints `wal` for its journal mode ([example](docs/usage-and-examples.md)).

## Where it fits

Sits under [base-tdb-helpers](https://github.com/TalkingDB/base-tdb-helpers) and every service; uses [base-tdb-models](https://github.com/TalkingDB/base-tdb-models) for its data shapes.

## Learn more

| Page | Read it to |
| :--- | :--- |
| [How it works](docs/architecture.md) | see the parts and how data moves |
| [Usage and examples](docs/usage-and-examples.md) | copy working examples |
| [Troubleshooting](docs/troubleshooting.md) | fix a problem |
| [Full reference](docs/reference.md) | read everything that used to be on this page |
| [All docs](docs/README.md) | see every page |

## Support TalkingDB

If base-tdb-clients saved you time, please [give it a star](https://github.com/TalkingDB/base-tdb-clients) ⭐. Stars help other developers find the project.

Found a bug, or a document it gets wrong? [Open an issue](https://github.com/TalkingDB/base-tdb-clients/issues/new). We are always here to help and open to a conversation. Explore the TalkingDB applications at [talkingdb.io](https://talkingdb.io/#applications).

## License

Licensed under the GNU Affero General Public License v3.0 ([AGPL-3.0](https://www.gnu.org/licenses/agpl-3.0.html)). See [LICENSE](LICENSE).
