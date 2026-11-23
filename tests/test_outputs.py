"""Verify that one offline run produces the complete numerical deliverable."""
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import pandas as pd

from run_analysis import run


class OutputTests(unittest.TestCase):
    def test_complete_output_set(self):
        with TemporaryDirectory() as folder:
            output = Path(folder)
            run(output)
            clinical = pd.read_csv(output / 'clinical/comparison.csv')
            samples = pd.read_csv(output / 'simulated/time_series.csv')
            convergence = pd.read_csv(output / 'simulated/convergence.csv')
            self.assertEqual(len(clinical), 2)
            self.assertEqual(len(samples), 1572)  # 4 * (31 + 61 + 301)
            self.assertEqual(len(convergence), 12)
            self.assertEqual(set(samples.data_type), {'simulated'})
            self.assertEqual(samples.groupby(['scenario', 'step_days']).time_days.max().tolist(),
                             [30.0] * 12)
            figures = list(output.rglob('*.png'))
            self.assertEqual(len(figures), 4)
            for path in figures:
                self.assertGreater(path.stat().st_size, 10_000)


if __name__ == '__main__':
    unittest.main()
