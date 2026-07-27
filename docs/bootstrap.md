# Stage 0 bootstrap contract

The repository is named Arx Mentis. Its distribution and Python import package are
`arx_mentis`; its command is `arx-mentis`. Version `0.1.0` is bootstrap metadata,
while the changelog remains Unreleased.

Stage 0 provides:

- installable Python 3.13+ packaging with no runtime dependencies;
- `version`, `doctor`, and `status` commands through both console and module entry
  points;
- importable boundary packages for the handwritten frontend, syntax, semantics,
  runtime, diagnostics, adapters, backends, Python reference backend, and future IR;
- policy, evidence, architecture, test, and decision documentation.

It explicitly provides no tokens, grammar, parser, AST nodes, name resolution,
checker, evaluator, runtime values, lowering, IR nodes, or backend implementation.
In particular, there is no `runtime/values.py` and no placeholder value class.

## Deferred bootstrap machinery

There is no lockfile, CI configuration, documentation generator, author metadata,
repository URL, release automation, parser implementation, or package adapter.
Those additions need a concrete use case. Publication remains out of scope, and
package-name availability must be checked when publication becomes concrete.

