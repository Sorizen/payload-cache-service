# payload-cache

A FastAPI microservice that builds a payload from two lists of strings. Every
string goes through a slow "transformer" (a stand-in for an external service),
the results are interleaved, and everything is cached in PostgreSQL so the
transformer is called as rarely as possible. `cache-cli` exercises the service
from the command line.

## Run with Docker

```bash
make up      # PostgreSQL, one-shot migrations, API on http://localhost:8000
make down
```

```bash
curl -X POST localhost:8000/payload -H 'content-type: application/json' \
  -d '{"list_1": ["first string", "second string"], "list_2": ["other string", "another string"]}'
# 201 {"id": "...", "message": "Payload created"}  (200 "Payload already exists" on a repeat)

curl localhost:8000/payload/<id>
# {"output": "FIRST STRING, OTHER STRING, SECOND STRING, ANOTHER STRING"}
```

Interactive docs: http://localhost:8000/docs.

## CLI

```bash
uv sync
uv run cache-cli -r 3 -j '{"list_1": ["a", "b"], "list_2": ["c", "d"]}'
cat payload.json | uv run cache-cli -o results.jsonl
```

| Flag | Meaning | Default |
|---|---|---|
| `-h`, `--host` | service URL | `http://localhost:8000` |
| `-r`, `--repeat` | number of iterations | `1` |
| `-i`, `--input` | input file, `-` for stdin | stdin |
| `-j`, `--json` | payload as a JSON string (not together with `-i`) | |
| `-o`, `--output` | output file, `-` for stdout | stdout |
| `--help` | show help | |

The task assigns `-h` to both `--host` and `--help`, which cannot work, so `-h`
is the host (as in `psql`) and help is `--help` only.

One JSON line is printed per iteration:
`{"iteration", "id", "created", "elapsed_ms", "output"}`. With `-r 3` the first
line has `created: true` and is slow, the others are `false` and fast: that is
the cache at work. Exit code 2 means invalid arguments, 1 means a network or
service error.

## Development

Requires Python 3.12, [uv](https://docs.astral.sh/uv/) and Docker (integration
tests start PostgreSQL with testcontainers).

```bash
make install    # virtualenv and dependencies
make check      # ruff, mypy --strict, pytest
```
