"""Single-compartment activity retention: analytical solution and forward Euler."""
import math

import numpy as np
import pandas as pd

# MIRDspecs Lu-177, Summary data / Radioactive decay. See data/clinical/SOURCES.md.
PHYSICAL_HALF_LIFE_DAYS = 6.647


def simulate(biological_half_life_days: float | None, step_days: float,
             duration_days: float = 30) -> tuple[pd.DataFrame, dict]:
    """Simulate A/A0 with hypothetical clearance, returning samples and errors.

    None means no biological removal. Activity is normalized to A0 = 1.
    A partial final step reaches the exact duration without overshooting.
    """
    for name, value in [('step_days', step_days), ('duration_days', duration_days),
                        ('biological_half_life_days', biological_half_life_days)]:
        if value is None and name == 'biological_half_life_days':
            continue
        if value is None or not math.isfinite(value) or value <= 0:
            raise ValueError(f'{name} must be finite and positive')

    physical_rate = math.log(2) / PHYSICAL_HALF_LIFE_DAYS
    biological_rate = (0.0 if biological_half_life_days is None
                       else math.log(2) / biological_half_life_days)
    rate = physical_rate + biological_rate
    if rate * min(step_days, duration_days) > 1:
        raise ValueError('Euler requires rate * time step <= 1 for nonnegative activity')
    if duration_days / step_days > 1_000_000:
        raise ValueError('Requested grid exceeds one million steps; use a larger step')

    # Exclude the endpoint first, then append it to avoid a duplicate final time.
    times = np.arange(0.0, duration_days, step_days)
    if len(times) > 1 and math.isclose(times[-1], duration_days, rel_tol=1e-14):
        times = times[:-1]
    times = np.append(times, duration_days)
    analytical = np.exp(-rate * times)
    euler = np.empty(len(times))
    euler[0] = 1.0
    for i in range(1, len(times)):
        dt = times[i] - times[i - 1]
        euler[i] = euler[i - 1] * max(0.0, 1.0 - rate * dt)

    # Integrating exact samples isolates quadrature error from Euler error.
    trapezoid = float(np.trapezoid(analytical, times))
    euler_integral = float(np.trapezoid(euler, times))
    exact = -math.expm1(-rate * duration_days) / rate
    label = ('physical_only' if biological_half_life_days is None
             else f'clearance_{biological_half_life_days:g}d')
    metadata = {
        'data_type': 'simulated', 'scenario': label,
        'biological_half_life_days': biological_half_life_days,
        'physical_half_life_days': PHYSICAL_HALF_LIFE_DAYS,
        'step_days': step_days, 'duration_days': duration_days,
    }
    samples = pd.DataFrame({
        **metadata, 'time_days': times,
        'analytical_fraction': analytical, 'euler_fraction': euler,
        'absolute_euler_error': np.abs(euler - analytical),
    })
    stats = {
        **metadata, 'effective_half_life_days': math.log(2) / rate,
        'exact_integral_days': exact, 'trapezoid_integral_days': trapezoid,
        'euler_trapezoid_integral_days': euler_integral,
        'trapezoid_absolute_error_days': abs(trapezoid - exact),
        'trapezoid_relative_error': abs(trapezoid - exact) / exact,
        'euler_integral_absolute_error_days': abs(euler_integral - exact),
        'euler_max_absolute_error': float(np.max(np.abs(euler - analytical))),
    }
    return samples, stats
