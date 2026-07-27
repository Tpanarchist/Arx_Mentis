# Backend equivalence obligations

No backend equivalence is claimed at Stage 0. Each obligation below is intentionally
unfilled. A future decision must define a backend-neutral observation method and
reference conformance tests before the status can change.

| Obligation | Status | Policy still required |
| --- | --- | --- |
| Results | Unfilled | Which owned results are equivalent, including structured and cyclic values? |
| Error identity and messages | Unfilled | Which error category, identity, span, payload, and message details are observable? |
| Side-effect order | Unfilled | Which effects are observable and what ordering relation must match? |
| I/O interleaving | Unfilled | How are stdout, stderr, input, buffering, and partial writes compared? |
| Float comparison | Unfilled | Are bit patterns, NaNs, signed zero, rounding, and tolerances significant? |
| Iteration order | Unfilled | Which collections promise order and how is nondeterminism compared? |
| Finalization order | Unfilled | Are cleanup and finalization observable, deterministic, or outside the language? |

Python's current behavior does not fill any row. Until a row is resolved, tests may
study backend behavior but may not promote that behavior to a language guarantee.

