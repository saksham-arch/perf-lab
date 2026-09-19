import unittest

from perf_lab import compare, compare_summaries, summarize


class SummaryTests(unittest.TestCase):
    def test_summarizes_samples(self) -> None:
        result = summarize([4, 1, 3, 2])
        self.assertEqual(result.count, 4)
        self.assertEqual(result.minimum, 1)
        self.assertEqual(result.median, 2.5)
        self.assertEqual(result.mean, 2.5)
        self.assertEqual(result.median_absolute_deviation, 1.0)
        self.assertEqual(result.relative_median_absolute_deviation, 0.4)
        self.assertEqual(result.p95, 4)
        self.assertEqual(result.maximum, 4)

    def test_rejects_invalid_samples(self) -> None:
        for samples in ([], [-1], [float("inf")]):
            with self.subTest(samples=samples), self.assertRaises(ValueError):
                summarize(samples)

    def test_compares_medians(self) -> None:
        baseline = summarize([10, 10, 10])
        candidate = summarize([11, 11, 11])
        self.assertAlmostEqual(compare(baseline, candidate), 0.1)

    def test_median_absolute_deviation_resists_outlier(self) -> None:
        result = summarize([10, 10, 11, 11, 1000])
        self.assertEqual(result.median_absolute_deviation, 1)

    def test_relative_dispersion_is_undefined_for_zero_median(self) -> None:
        result = summarize([0, 0, 1])
        self.assertIsNone(result.relative_median_absolute_deviation)

    def test_classifies_practical_median_change(self) -> None:
        baseline = summarize([100, 100, 100])
        slower = compare_summaries(
            baseline, summarize([110, 110, 110]), practical_threshold=0.05
        )
        similar = compare_summaries(
            baseline, summarize([103, 103, 103]), practical_threshold=0.05
        )
        self.assertEqual(slower.outcome, "slower")
        self.assertAlmostEqual(slower.relative_change, 0.1)
        self.assertEqual(similar.outcome, "no_material_change")

    def test_validates_practical_threshold(self) -> None:
        summary = summarize([1])
        with self.assertRaises(ValueError):
            compare_summaries(summary, summary, practical_threshold=-0.1)


if __name__ == "__main__":
    unittest.main()
