from dataclasses import dataclass
from math import ceil, isfinite
from statistics import fmean, median
from typing import Iterable, Optional


@dataclass(frozen=True)
class Summary:
    count: int
    minimum: float
    median: float
    mean: float
    median_absolute_deviation: float
    relative_median_absolute_deviation: Optional[float]
    p95: float
    maximum: float


@dataclass(frozen=True)
class Comparison:
    baseline_median: float
    candidate_median: float
    absolute_change: float
    relative_change: float
    practical_threshold: float
    outcome: str
    baseline_p95: float
    candidate_p95: float
    p95_absolute_change: float
    p95_relative_change: float
    p95_outcome: str


def _samples(values: Iterable[float]) -> list[float]:
    result = [float(value) for value in values]
    if not result:
        raise ValueError("at least one sample is required")
    if any(not isfinite(value) or value < 0 for value in result):
        raise ValueError("samples must be finite and non-negative")
    return sorted(result)


def summarize(values: Iterable[float]) -> Summary:
    samples = _samples(values)
    p95_index = ceil(0.95 * len(samples)) - 1
    sample_median = median(samples)
    median_absolute_deviation = median(
        abs(sample - sample_median) for sample in samples
    )
    return Summary(
        count=len(samples),
        minimum=samples[0],
        median=sample_median,
        mean=fmean(samples),
        median_absolute_deviation=median_absolute_deviation,
        relative_median_absolute_deviation=(
            median_absolute_deviation / sample_median
            if sample_median > 0
            else None
        ),
        p95=samples[p95_index],
        maximum=samples[-1],
    )


def compare(baseline: Summary, candidate: Summary) -> float:
    """Return median change as a ratio; positive values indicate slowdown."""
    if baseline.median == 0:
        raise ValueError("baseline median must be greater than zero")
    return candidate.median / baseline.median - 1


def _classify_change(relative_change: float, practical_threshold: float) -> str:
    if relative_change > practical_threshold:
        return "slower"
    if relative_change < -practical_threshold:
        return "faster"
    return "no_material_change"


def compare_summaries(
    baseline: Summary,
    candidate: Summary,
    *,
    practical_threshold: float = 0.05,
) -> Comparison:
    """Classify median movement against a caller-chosen practical threshold."""
    if not isfinite(practical_threshold) or practical_threshold < 0:
        raise ValueError("practical_threshold must be finite and non-negative")
    relative_change = compare(baseline, candidate)
    p95_relative_change = candidate.p95 / baseline.p95 - 1
    return Comparison(
        baseline.median,
        candidate.median,
        candidate.median - baseline.median,
        relative_change,
        practical_threshold,
        _classify_change(relative_change, practical_threshold),
        baseline.p95,
        candidate.p95,
        candidate.p95 - baseline.p95,
        p95_relative_change,
        _classify_change(p95_relative_change, practical_threshold),
    )
