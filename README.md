# perf-lab

Small, dependency-free building blocks for analyzing repeatable performance
experiments. It summarizes timing samples with median, mean, nearest-rank p95,
median absolute deviation (MAD), and relative MAD, and compares a candidate
run with a baseline without claiming statistical significance.

```bash
python -m unittest discover -s tests
python -m perf_lab 0.101 0.099 0.105 0.100
```

All input values must use the same unit. Percentiles use the nearest-rank
definition, which keeps results deterministic for small benchmark samples.
Relative MAD divides MAD by the median so dispersion can be compared across
different timing scales. It is reported as `null` when the median is zero,
where that ratio is undefined.

`compare_summaries` can label median movement as `faster`, `slower`, or
`no_material_change` using a caller-selected practical threshold. It also
reports the absolute and relative p95 movement so tail behavior is not hidden
by the median. Median and p95 movement receive separate outcomes using the same
practical threshold, so a stable median cannot hide a tail regression. Both
labels are descriptive effect-size rules, not statistical significance tests;
nearest-rank p95 remains sensitive to sample count and workload composition.
