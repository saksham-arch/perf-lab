import unittest

from perf_lab import compare, summarize


class SummaryTests(unittest.TestCase):
    def test_summarizes_samples(self) -> None:
        result = summarize([4, 1, 3, 2])
        self.assertEqual(result.count, 4)
        self.assertEqual(result.minimum, 1)
        self.assertEqual(result.median, 2.5)
        self.assertEqual(result.mean, 2.5)
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


if __name__ == "__main__":
    unittest.main()
