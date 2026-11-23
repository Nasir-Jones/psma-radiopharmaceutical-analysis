"""Run from any working directory to recreate all project tables and figures."""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use('Agg')  # Save figures without requiring a desktop plotting window.
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.clinical import ENDPOINTS, load_clinical, summarize_clinical
from src.simulation import simulate

ROOT = Path(__file__).resolve().parent
SCENARIOS = (None, 1, 3, 7)
STEPS = (1.0, 0.5, 0.1)
COLORS = ('#475569', '#d97706', '#0f766e', '#7c3aed')
LABELS = ('No biological clearance', '1-day clearance half-life',
          '3-day clearance half-life', '7-day clearance half-life')


def save_figure(fig, path: Path, note: str) -> None:
    """Reserve space for a source/interpretation note beneath each chart."""
    fig.text(0.06, 0.025, note, fontsize=9, color='#475569', va='bottom')
    fig.tight_layout(rect=(0, 0.12, 1, 0.92))
    fig.savefig(path, dpi=160, facecolor='white')
    plt.close(fig)


def plot_clinical(data: pd.DataFrame, folder: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(11, 5.8))
    titles = ('Overall survival', 'Imaging-based progression-free survival')
    for ax, endpoint, title in zip(axes, ENDPOINTS, titles):
        group = data.loc[data.endpoint == endpoint].set_index('arm').loc[['control', 'treatment']]
        values = group.median_months.to_numpy()
        errors = np.array([values - group.ci_low_months, group.ci_high_months - values])
        ax.bar([0, 1], values, yerr=errors, capsize=6,
               color=['#94a3b8', '#0f766e'], width=0.58)
        for x, (_, row) in enumerate(group.iterrows()):
            ax.text(x, 0.25, f'{row.median_months:g} months\nn = {int(row.n)}',
                    ha='center', va='bottom', fontsize=10, color='white', weight='bold')
        ax.set_xticks([0, 1], ['Standard care', 'Lu-177-PSMA-617\n+ standard care'])
        ax.set_title(f'{title}\nPublished {group.ci_level_percent.iloc[0]:g}% confidence intervals', fontsize=11)
        ax.set_ylabel('Reported median (months)')
        ax.set_ylim(0, 19)
        ax.grid(axis='y', alpha=0.15)
        ax.set_axisbelow(True)
    fig.suptitle('VISION trial | Published clinical summaries', fontsize=16, weight='bold')
    save_figure(fig, folder / 'median_outcomes.png',
                'Source: Sartor et al. (2021), Figure 2; EMA assessment section 3.2. See data/clinical/SOURCES.md.\n'
                'Different endpoint populations; median differences do not describe individual patient benefit.')


def plot_simulation(samples: pd.DataFrame, stats: pd.DataFrame, folder: Path) -> None:
    fig, ax = plt.subplots(figsize=(10, 5.8))
    scenario_names = list(stats.scenario.drop_duplicates())
    for name, color, label in zip(scenario_names, COLORS, LABELS):
        fine = samples.loc[(samples.scenario == name) & (samples.step_days == 0.1)]
        coarse = samples.loc[(samples.scenario == name) & (samples.step_days == 1)]
        ax.plot(fine.time_days, fine.analytical_fraction, color=color, label=label)
        ax.plot(coarse.time_days, coarse.euler_fraction, 'o', ms=3, color=color, alpha=0.65)
    ax.set(xlabel='Time after hypothetical administration (days)',
           ylabel='Retained activity / initial activity', xlim=(0, 30), ylim=(0, 1.04))
    ax.legend(frameon=False)
    ax.grid(alpha=0.15)
    fig.suptitle('SIMULATED | Decay and biological clearance', fontsize=16, weight='bold')
    save_figure(fig, folder / 'activity_retention.png',
                'Lines: analytical solution. Dots: forward Euler with a 1-day step. Lu-177 physical half-life: 6.647 days (MIRDspecs).\n'
                'Clearance half-lives are hypothetical. Activity retention is not a clinical efficacy prediction.')

    fine_stats = stats.loc[stats.step_days == 0.1]
    fig, ax = plt.subplots(figsize=(10, 5.8))
    positions = np.arange(4)
    ax.bar(positions - 0.18, fine_stats.exact_integral_days, width=0.36,
           color='#0f766e', label='Analytical integral')
    ax.bar(positions + 0.18, fine_stats.trapezoid_integral_days, width=0.36,
           color='#94a3b8', label='Trapezoidal rule, 0.1-day step')
    for x, value in zip(positions, fine_stats.exact_integral_days):
        ax.text(x, value + 0.16, f'{value:.3f}', ha='center')
    ax.set_xticks(positions, ['No clearance', '1 day', '3 days', '7 days'])
    ax.set(xlabel='Hypothetical biological clearance half-life',
           ylabel='Normalized cumulative activity over 30 days (days)')
    ax.set_ylim(0, fine_stats.exact_integral_days.max() * 1.25)
    ax.legend(frameon=False)
    ax.grid(axis='y', alpha=0.15)
    ax.set_axisbelow(True)
    fig.suptitle('SIMULATED | Cumulative activity', fontsize=16, weight='bold')
    save_figure(fig, folder / 'cumulative_activity.png',
                'Integral of A(t)/A0 from day 0 to day 30. Numerical bars integrate analytical samples to isolate quadrature error.\n'
                'Units are days; these values are neither absorbed dose nor measured clinical benefit.')

    fig, axes = plt.subplots(1, 2, figsize=(11, 5.8))
    for name, color, label in zip(scenario_names, COLORS, LABELS):
        group = stats.loc[stats.scenario == name].sort_values('step_days')
        axes[0].loglog(group.step_days, group.euler_max_absolute_error, 'o-', color=color, label=label)
        axes[1].loglog(group.step_days, group.trapezoid_relative_error, 'o-', color=color)
    axes[0].set(title='Forward Euler', ylabel='Maximum absolute error in activity fraction')
    axes[1].set(title='Trapezoidal integration of exact samples', ylabel='Relative integral error (fraction)')
    for ax in axes:
        ax.set_xlabel('Time step (days)')
        ax.set_xticks([0.1, 0.5, 1], ['0.1', '0.5', '1.0'])
        ax.grid(which='both', alpha=0.15)
    axes[0].legend(frameon=False, fontsize=9)
    fig.suptitle('SIMULATED | Smaller steps reduce numerical error', fontsize=16, weight='bold')
    save_figure(fig, folder / 'numerical_convergence.png',
                'Errors use analytical references over 30 days. Euler updates activity; trapezoidal integration uses analytical samples.\n'
                'First-order Euler and second-order trapezoidal convergence are expected as the step tends to zero.')


def run(output_dir: Path) -> None:
    """Create all outputs from local clinical inputs and deterministic models."""
    output_dir = Path(output_dir)
    clinical_dir, simulated_dir = output_dir / 'clinical', output_dir / 'simulated'
    clinical_dir.mkdir(parents=True, exist_ok=True)
    simulated_dir.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10,
                         'axes.spines.top': False, 'axes.spines.right': False})

    data = load_clinical(ROOT / 'data/clinical/vision_summary.csv')
    comparison = summarize_clinical(data)
    comparison.to_csv(clinical_dir / 'comparison.csv', index=False, float_format='%.10g')
    plot_clinical(data, clinical_dir)

    sample_tables, summary_rows = [], []
    for biological_half_life in SCENARIOS:
        for step in STEPS:
            samples, summary = simulate(biological_half_life, step)
            sample_tables.append(samples)
            summary_rows.append(summary)
    all_samples, convergence = pd.concat(sample_tables, ignore_index=True), pd.DataFrame(summary_rows)
    all_samples.to_csv(simulated_dir / 'time_series.csv', index=False, float_format='%.10g')
    convergence.to_csv(simulated_dir / 'convergence.csv', index=False, float_format='%.10g')
    plot_simulation(all_samples, convergence, simulated_dir)

    print('PUBLISHED CLINICAL SUMMARY (descriptive differences of medians):')
    print(comparison[['endpoint', 'median_difference_months']].to_string(index=False))
    print('\nSIMULATION: four hypothetical clearance scenarios x three step sizes.')
    print(f'Wrote {len(all_samples)} simulated samples and four figures to {output_dir.resolve()}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'results')
    run(parser.parse_args().output_dir)
