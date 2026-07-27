"""Run a small human-readable witness of the Euclid I.1 experiment."""

from __future__ import annotations

from .model import (
    Effect,
    IntersectionPoint,
    Potential,
    Side,
    cast,
    make_context,
    make_proposition,
)


def _apex_side(effect: Effect) -> str:
    apex = next(
        point for point in effect.form.points if isinstance(point, IntersectionPoint)
    )
    return apex.side.value


def main() -> None:
    line_ab, spell = make_proposition()
    unresolved = cast(spell, make_context(line_ab))
    print(f"inspected Spell: {spell.name} ({len(spell.steps)} exact steps)")
    if isinstance(unresolved, Potential):
        sides = sorted(_apex_side(effect) for effect in unresolved.options)
        print(f"unoriented Cast: Potential options={sides}")
        print("trigger: orientation declared by Context")
    for side in Side:
        result = cast(spell, make_context(line_ab, selected_side=side))
        if isinstance(result, Effect):
            print(
                f"{side.value}-oriented Cast: "
                f"Effect={_apex_side(result)}, "
                f"demonstration steps={len(result.demonstration.steps)}"
            )


if __name__ == "__main__":
    main()
