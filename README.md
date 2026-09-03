# perf-lab

Small, dependency-free building blocks for analyzing repeatable performance
experiments. It summarizes timing samples with median, mean, nearest-rank p95,
and median absolute deviation (MAD), and compares a candidate run with a
baseline without claiming statistical significance.

```bash
python -m unittest discover -s tests
python -m perf_lab 0.101 0.099 0.105 0.100
```

All input values must use the same unit. Percentiles use the nearest-rank
definition, which keeps results deterministic for small benchmark samples.
