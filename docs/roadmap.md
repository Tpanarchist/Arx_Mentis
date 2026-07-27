# Roadmap

This order is a constraint on learning, not a release schedule.

1. Preserve Stage 0 packaging, diagnostic boundaries, evidence records, and open
   decisions.
2. Formalize only the Forms needed by Euclid I.1 in a disposable experiment.
3. Model its Spell as one inspectable Form with declared Will and requirements.
4. Cast that same Form through an explicit Context without mutating the given Forms.
5. Produce a new Effect, compare it with Will, and trace its Demonstration to named
   Definitions, Postulates, and Common Notions.
6. Expose the two circle intersections as `Potential(options, trigger)` when Context
   provides no orientation; test that no host-language ordering is exposed as a
   default.
7. Record representational friction and revise or reject the provisional foundation
   where the executable proposition does not support it.
8. Design the smallest source notation capable of expressing the distinctions the
   experiment actually needed, with spans originating at the first token.
9. Only then introduce parsing, checking, owned runtime values, evaluation, lowering,
   IR discovery, and backend selection through the existing reversible seams.

The typed checked representation must still precede freezing evaluation order,
equality, mutability, or error propagation. Those choices need typed programs and
observable examples; deciding them from untyped evaluator convenience would make
reversal needlessly expensive.

## Primary foundation probe

Euclid I.1 is the first horizontal probe because one small construction crosses
Point, Line, Form, Will, Spell, Cast, Effect, Context, Potential, Demonstration, Ars,
and code/data identity. It lives under `experiments/euclid_i_1` and is evidence, not
a permanent API.

Self-hosting the tokenizer and parser remains a useful later horizontal probe after
there is evidence for the notation they would process.

Package adapters are optional and late. They should follow a stable semantic core
and a concrete interoperability need, never drive core naming or value semantics.
