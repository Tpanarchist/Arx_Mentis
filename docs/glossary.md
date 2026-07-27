# Glossary

**Accepted decision**
: A choice recorded by an Accepted ADR. It can change through a superseding ADR,
  but implementations may rely on it until then.

**Arx Mentis value**
: A semantic result represented by a project-owned abstraction. Its implementation
  may use Python internally; a bare Python object is not itself an Arx Mentis value.

**Backend**
: A consumer of typed checked representations. Reference evaluation and future IR
  lowering are sibling backend paths.

**Checked representation**
: The future typed output of resolution and checking, suitable for backend
  consumption. No shape is selected at Stage 0.

**Evidence trigger**
: Three genuinely unrelated occurrences of the same nameable tension, making thesis
  synthesis warranted but not mandatory.

**Horizontal probe**
: A narrow program that exercises many language layers. The early primary probe is
  self-hosting the tokenizer and then the parser.

**Lowering sketch**
: A short attempted mapping from a feature to simpler constructs that records both
  successes and semantic losses. It is required before an IR exists.

**Open question**
: A deliberately unresolved choice with an owner or resolution trigger. Python
  behavior does not answer it implicitly.

**Reversible seam**
: A boundary that localizes an unsettled choice so the implementation can change
  without redefining observable language behavior.

**Span**
: Source provenance beginning at tokenization and retained through parsing,
  resolution, and checking.

