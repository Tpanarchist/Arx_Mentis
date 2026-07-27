# Glossary

**Ars**
: An organized body of Definitions, Postulates, Common Notions, Forms, Spells,
  Casts, Effects, Demonstrations, and unresolved Potentials.

**Accepted decision**
: A choice recorded by an Accepted ADR. It can change through a superseding ADR,
  but implementations may rely on it until then.

**Arx Mentis value**
: A semantic result represented by a project-owned abstraction. Its implementation
  may use Python internally; a bare Python object is not itself an Arx Mentis value.

**Backend**
: A consumer of typed checked representations. Reference evaluation and future IR
  lowering are sibling backend paths.

**Cast**
: The performance of a Spell within an explicit Context.

**Checked representation**
: The future typed output of resolution and checking, suitable for backend
  consumption. No shape is selected at Stage 0.

**Context**
: The named Reader, Forms, permissions, constructions, conditions, Potentials, and
  evidence available to a Cast.

**Effect**
: The actual Form or change produced by a Cast, kept distinct from intended Will.

**Evidence trigger**
: Three genuinely unrelated occurrences of the same nameable tension, making thesis
  promotion or broader synthesis warranted but not mandatory.

**Form**
: An intelligible arrangement of Points and Lines. Data, instructions, Spells,
  Definitions, proofs, and Effects share this substance and differ by reading role.

**Line**
: An explicit relation or passage between Points. Direction, order, distance, and
  other possible properties remain open questions.

**Horizontal probe**
: A narrow program that exercises many language layers. Euclid I.1 is the first
  foundation probe; tokenizer and parser self-hosting remains a later probe.

**Lowering sketch**
: A short attempted mapping from a feature to simpler constructs that records both
  successes and semantic losses. It is required before an IR exists.

**Open question**
: A deliberately unresolved choice with an owner or resolution trigger. Python
  behavior does not answer it implicitly.

**Point**
: The smallest settled distinction the system can address: a definite here rather
  than elsewhere.

**Potential**
: Unsettled alternative Forms represented by exactly their options and the trigger
  that could legitimately settle among them; it has no selected default.

**Reversible seam**
: A boundary that localizes an unsettled choice so the implementation can change
  without redefining observable language behavior.

**Span**
: Source provenance beginning at tokenization and retained through parsing,
  resolution, and checking.

**Spell**
: A Form read as the exact construction intended to serve a declared Will.

**Will**
: The intended Form or change against which an actual Effect can be judged.
