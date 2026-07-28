"""Reports are filtered presentations of unchanged event streams."""

from __future__ import annotations

from .outcomes import EventStream, Report, ReportKind, ReportPolicy


def make_report(stream: EventStream, policy: ReportPolicy | None = None) -> Report:
    declared = policy or stream.plan.report_policy
    if declared.kind is ReportKind.ALL:
        trials = stream.trials
    else:
        trials = tuple(
            trial for trial in stream.trials if trial.outcome is declared.target
        )
    return Report(stream, declared, trials)
