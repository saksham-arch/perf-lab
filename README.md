# perf-lab

Small, dependency-free building blocks for analyzing repeatable performance
experiments. It summarizes timing samples with median, mean, nearest-rank
quartiles and p95, median absolute deviation (MAD), and relative dispersion,
and compares a candidate run with a baseline without claiming statistical
significance.

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
PYTHONPATH=src python3 -m perf_lab 0.101 0.099 0.105 0.100
```

All input values must use the same unit. Percentiles use the nearest-rank
definition, which keeps results deterministic for small benchmark samples.
Relative MAD divides MAD by the median so dispersion can be compared across
different timing scales. It is reported as `null` when the median is zero,
where that ratio is undefined.
The interquartile range (IQR) is the nearest-rank third quartile minus the first
quartile. Relative IQR divides that spread by the median and is `null` when the
median is zero. IQR describes the central half of the observed samples and can
hide important tail behavior, so inspect it alongside p95, extrema, and raw
measurements rather than treating it as a stability guarantee.

`compare_summaries` can label median movement as `faster`, `slower`, or
`no_material_change` using a caller-selected practical threshold. It also
reports the absolute and relative p95 movement so tail behavior is not hidden
by the median. Median and p95 movement receive separate outcomes using the same
practical threshold, so a stable median cannot hide a tail regression. Both
labels are descriptive effect-size rules, not statistical significance tests;
nearest-rank p95 remains sensitive to sample count and workload composition.
Comparisons retain both sample counts and report candidate-to-baseline
`sample_count_ratio`. Unequal counts are not automatically invalid, but the
imbalance is visible because it can change percentile resolution and confidence
in the observed summaries. They also retain both relative MAD values and their
candidate-minus-baseline difference. A positive dispersion difference means
the candidate samples varied more relative to their median; it is not a
significance test and is `null` when either median is zero.
