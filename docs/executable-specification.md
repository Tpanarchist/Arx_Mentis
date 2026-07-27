# Python executable specification

Python is the first executable reference specification for Arx Mentis. This means a
small, readable implementation will make proposed behavior concrete and testable. It
does not mean Python is the language definition or the required long-term backend.

## Authority and limits

Accepted examples and conformance tests state expected observable behavior. The
Python reference implementation demonstrates one implementation of that behavior.
When its host-language behavior is not covered by an accepted language decision,
the behavior remains accidental and must not be relied upon.

Implementation shortcuts may use Python internally only behind owned interfaces.
Raw Python values, exceptions, iteration order, finalizers, and I/O buffering must
not escape as semantic answers. Unsettled cross-backend behavior is tracked in
`equivalence.md` rather than inferred from CPython.

## Review questions

For each new evaluator path, ask:

- Which result and error objects cross the semantic boundary?
- Which Python behavior could be observed by a program or test?
- Does a conformance example state that observation intentionally?
- Can a future backend implement the same contract without emulating unrelated
  Python details?

