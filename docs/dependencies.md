# Dependency policy

Arx Mentis has no runtime dependencies at Stage 0. Hatchling is the build backend;
pytest and Ruff are development-only tools.

Awesome Python and similar catalogs are advisory discovery aids, not approval lists.
Before adding any dependency, record:

| Question | Required justification |
| --- | --- |
| Purpose | What concrete project problem does it solve now? |
| Permanence | Is it disposable exploration, a development tool, or a lasting runtime dependency? |
| Alternatives | Why are the standard library, a small owned implementation, and other candidates insufficient? |
| Semantic leakage | Could its API, data model, exceptions, ordering, numeric behavior, or lifecycle become observable language behavior? |
| Exit cost | What code/data boundary makes replacement practical? |
| Supply risk | What maintenance, licensing, security, platform, and release risks does it add? |

Runtime additions require especially strong evidence. A dependency must remain
behind an Arx Mentis-owned interface when exposing it directly would constrain
language semantics. Package adapters do not justify moving a third-party API into
the core.

