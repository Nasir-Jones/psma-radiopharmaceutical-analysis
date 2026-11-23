"""Use exact physics as an independent numerical reference."""
import math
import unittest

import numpy as np

from src.simulation import PHYSICAL_HALF_LIFE_DAYS, simulate


class SimulationTests(unittest.TestCase):
    def test_half_life_and_exact_integral(self):
        half = PHYSICAL_HALF_LIFE_DAYS
        samples, stats = simulate(None, 0.1, duration_days=half)
        self.assertAlmostEqual(samples.iloc[-1].analytical_fraction, 0.5)
        self.assertAlmostEqual(stats['exact_integral_days'], half / (2 * math.log(2)))
        self.assertEqual(samples.iloc[0].euler_fraction, 1)

    def test_clearance_reduces_retention(self):
        physical, base = simulate(None, 0.1)
        cleared, stats = simulate(3, 0.1)
        self.assertTrue(np.all(cleared.analytical_fraction <= physical.analytical_fraction))
        self.assertLess(stats['exact_integral_days'], base['exact_integral_days'])
        self.assertTrue(np.all(np.diff(cleared.euler_fraction) <= 0))
        self.assertTrue(np.all(cleared.euler_fraction >= 0))

    def test_convergence(self):
        for biological in [None, 1, 3, 7]:
            stats = [simulate(biological, step)[1] for step in [1, 0.5, 0.1]]
            for key in ['euler_max_absolute_error', 'trapezoid_absolute_error_days']:
                self.assertGreater(stats[0][key], stats[1][key])
                self.assertGreater(stats[1][key], stats[2][key])
            self.assertLess(stats[-1]['euler_max_absolute_error'], 0.016)
            self.assertLess(stats[-1]['trapezoid_relative_error'], 0.001)

    def test_partial_step_and_short_duration(self):
        for duration, step in [(1, 0.3), (0.05, 0.1)]:
            samples, _ = simulate(None, step, duration_days=duration)
            self.assertEqual(samples.iloc[-1].time_days, duration)
            self.assertTrue(np.all(np.diff(samples.time_days) > 0))
            self.assertTrue(np.all(samples.time_days <= duration))

    def test_invalid_parameters_and_positivity(self):
        for invalid in [0, -1, math.nan, math.inf]:
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    simulate(invalid, 0.1)
                with self.assertRaises(ValueError):
                    simulate(None, invalid)
                with self.assertRaises(ValueError):
                    simulate(None, 0.1, duration_days=invalid)
        with self.assertRaises(ValueError):
            simulate(1, 2)


if __name__ == '__main__':
    unittest.main()
