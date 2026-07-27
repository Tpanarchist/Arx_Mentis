# Arx Mentis

Arx Mentis is a language-design project at **Stage 0**. This repository contains
only the executable bootstrap, architectural boundaries, decision records, and
evidence practices needed to explore the language without turning Python behavior
into accidental language semantics.

The distribution and import package are `arx_mentis`; the installed command is
`arx-mentis`. The bootstrap requires Python 3.13 or newer and is licensed under
Apache-2.0.

```console
python -m pip install -e ".[dev]"
arx-mentis version
arx-mentis doctor
arx-mentis status
python -m arx_mentis status
```

Stage 0 intentionally implements no syntax, AST, semantics, evaluator, runtime
values, or IR. Start with [the documentation map](docs/README.md), especially the
[bootstrap contract](docs/bootstrap.md) and
[development process](docs/development-process.md).

