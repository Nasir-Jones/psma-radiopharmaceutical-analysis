"""Check descriptive calculations and reject misleading input tables."""
from pathlib import Path
import unittest

import numpy as np
import pandas as pd

from src.clinical import load_clinical, summarize_clinical

DATA = Path(__file__).resolve().parents[1] / 'data/clinical/vision_summary.csv'


class ClinicalTests(unittest.TestCase):
    def setUp(self):
        self.data = load_clinical(DATA)

    def test_published_values_and_distinct_populations(self):
        result = summarize_clinical(self.data).set_index('endpoint')
        self.assertAlmostEqual(result.loc['overall_survival', 'median_difference_months'], 4.0)
        self.assertAlmostEqual(result.loc['imaging_pfs', 'median_difference_months'], 5.3)
        self.assertEqual(result.loc['overall_survival', 'treatment_n'], 551)
        self.assertEqual(result.loc['imaging_pfs', 'treatment_n'], 385)
        self.assertEqual(result.loc['overall_survival', 'control_n'], 280)
        self.assertEqual(result.loc['imaging_pfs', 'control_n'], 196)
        self.assertEqual(result.loc['imaging_pfs', 'ci_level_percent'], 99.2)

    def test_missing_duplicate_and_unknown_arms(self):
        cases = [self.data.iloc[:-1], pd.concat([self.data, self.data.iloc[:1]])]
        unknown = self.data.copy()
        unknown.loc[0, 'arm'] = 'other'
        cases.append(unknown)
        for case in cases:
            with self.subTest(case=case.shape), self.assertRaises(ValueError):
                summarize_clinical(case)

    def test_invalid_numbers_and_intervals(self):
        for column, value in [('median_months', -1), ('median_months', np.nan),
                              ('n', 1.5), ('n', np.inf), ('ci_low_months', 100),
                              ('hazard_ratio', 0), ('ci_level_percent', 101)]:
            case = self.data.copy()
            case[column] = case[column].astype(float)
            case.loc[0, column] = value
            with self.subTest(column=column, value=value), self.assertRaises(ValueError):
                summarize_clinical(case)

    def test_missing_columns_and_inconsistent_metadata(self):
        with self.assertRaises(ValueError):
            summarize_clinical(self.data.drop(columns='source_url'))
        for column, value in [('population', 'different population'),
                              ('ci_level_percent', 90), ('hazard_ratio', 0.8),
                              ('unit', 'days'), ('source_url', '')]:
            case = self.data.copy()
            case.loc[0, column] = value
            with self.subTest(column=column), self.assertRaises(ValueError):
                summarize_clinical(case)


if __name__ == '__main__':
    unittest.main()
