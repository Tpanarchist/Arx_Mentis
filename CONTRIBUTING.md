# Contributing

Arx Mentis is in Stage 0. Read `docs/development-process.md` before proposing a
language feature. A feature is not accepted on intuition alone: its implementation
work must carry evidence, examples, tests, and a short lowering sketch.

Use Python 3.13 or newer, install `.[dev]`, and run:

```console
python -m pytest
python -m ruff check .
python -m ruff format --check .
python -m pip check
```

Keep unrelated changes separate. Do not add runtime dependencies without updating
`docs/dependencies.md`, and do not expose a raw Python object as an Arx Mentis
semantic value.

