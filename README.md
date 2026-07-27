# Arx Mentis

Arx Mentis is a language-design project at **Stage 0** exploring exact, inspectable
construction through Point, Line, Form, Will, Spell, Cast, Context, Effect,
Potential, and Ars. Its [foundation](docs/foundation.md) is provisional: executable
experiments must test its distinctions before syntax or implementation choices are
allowed to harden around them.

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

Stage 0 intentionally implements no syntax, AST, permanent semantics, evaluator,
runtime values, or IR. The first disposable probe models Euclid I.1 without entering
the installable package:

```console
python -m experiments.euclid_i_1
python -m pytest tests/experiments/test_euclid_i_1.py
```

Start with [the documentation map](docs/README.md), the
[foundation](docs/foundation.md), and the
[experiment contract](experiments/euclid_i_1/README.md).
