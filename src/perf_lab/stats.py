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
    p95: float
    maximum: float


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
    return Summary(
        count=len(samples),
        minimum=samples[0],
        median=median(samples),
        mean=fmean(samples),
        p95=samples[p95_index],
        maximum=samples[-1],
    )


def compare(baseline: Summary, candidate: Summary) -> float:
    """Return median change as a ratio; positive values indicate slowdown."""
    if baseline.median == 0:
        raise ValueError("baseline median must be greater than zero")
    return candidate.median / baseline.median - 1

