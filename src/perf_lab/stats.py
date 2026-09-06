from dataclasses import dataclass
from math import ceil, isfinite
from statistics import fmean, median
from typing import Iterable


@dataclass(frozen=True)
class Summary:
    count: int
    minimum: float
    median: float
    mean: float
    median_absolute_deviation: float
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
    return Summary(
        count=len(samples),
        minimum=samples[0],
        median=sample_median,
        mean=fmean(samples),
        median_absolute_deviation=median(
            abs(sample - sample_median) for sample in samples
        ),
        p95=samples[p95_index],
        maximum=samples[-1],
    )


def compare(baseline: Summary, candidate: Summary) -> float:
    """Return median change as a ratio; positive values indicate slowdown."""
    if baseline.median == 0:
        raise ValueError("baseline median must be greater than zero")
    return candidate.median / baseline.median - 1


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
    if relative_change > practical_threshold:
        outcome = "slower"
    elif relative_change < -practical_threshold:
        outcome = "faster"
    else:
        outcome = "no_material_change"
    return Comparison(
        baseline.median,
        candidate.median,
        candidate.median - baseline.median,
        relative_change,
        practical_threshold,
        outcome,
    )
