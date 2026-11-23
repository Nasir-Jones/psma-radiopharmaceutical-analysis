"""Describe published aggregate outcomes without inventing patient data."""
from pathlib import Path

import numpy as np
import pandas as pd

ENDPOINTS = ('overall_survival', 'imaging_pfs')
NUMERIC = ('n', 'median_months', 'ci_low_months', 'ci_high_months',
           'ci_level_percent', 'hazard_ratio', 'hr_ci_low', 'hr_ci_high')
TEXT = ('endpoint', 'arm', 'unit', 'population', 'source_url',
        'source_location', 'interval_source_url')


def load_clinical(path: Path) -> pd.DataFrame:
    """Read and validate the curated CSV; no network is needed."""
    data = pd.read_csv(path)
    summarize_clinical(data)
    return data


def summarize_clinical(data: pd.DataFrame) -> pd.DataFrame:
    """Return one descriptive treatment/control comparison per endpoint."""
    missing = set(NUMERIC + TEXT) - set(data.columns)
    if missing:
        raise ValueError(f'Missing clinical columns: {sorted(missing)}')
    data = data.copy()
    for column in TEXT:
        if data[column].isna().any() or data[column].astype(str).str.strip().eq('').any():
            raise ValueError(f'Clinical column {column} must not be empty')
    for column in NUMERIC:
        data[column] = pd.to_numeric(data[column], errors='coerce')
        if not np.isfinite(data[column]).all() or (data[column] <= 0).any():
            raise ValueError(f'Clinical column {column} requires finite positive values')
    if (data.n % 1 != 0).any() or (data.ci_level_percent >= 100).any():
        raise ValueError('Sample sizes must be integers and CI levels must be below 100')
    if not data.unit.eq('months').all():
        raise ValueError('Clinical survival values must be in months')
    for value, low, high in [('median_months', 'ci_low_months', 'ci_high_months'),
                             ('hazard_ratio', 'hr_ci_low', 'hr_ci_high')]:
        if ((data[low] > data[value]) | (data[value] > data[high])).any():
            raise ValueError(f'{value} must lie within its interval')
    if set(data.endpoint) != set(ENDPOINTS):
        raise ValueError('Expected overall_survival and imaging_pfs endpoints')

    rows = []
    shared = ('population', 'ci_level_percent', 'hazard_ratio', 'hr_ci_low',
              'hr_ci_high', 'source_url', 'interval_source_url')
    for endpoint in ENDPOINTS:
        group = data.loc[data.endpoint == endpoint]
        if len(group) != 2 or set(group.arm) != {'treatment', 'control'}:
            raise ValueError(f'{endpoint} requires exactly one row per arm')
        if any(group[column].nunique() != 1 for column in shared):
            raise ValueError(f'{endpoint} has inconsistent comparison metadata')
        arms = group.set_index('arm')
        treatment, control = arms.loc['treatment'], arms.loc['control']
        rows.append({
            'data_type': 'published_clinical_summary', 'endpoint': endpoint,
            'treatment_n': int(treatment.n), 'control_n': int(control.n),
            'treatment_median_months': treatment.median_months,
            'control_median_months': control.median_months,
            'median_difference_months': treatment.median_months - control.median_months,
            **{column: treatment[column] for column in shared},
        })
    return pd.DataFrame(rows)
