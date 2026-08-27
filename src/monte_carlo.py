"""Run repeated failure scenarios and summarise systemic losses."""

import numpy as np
import pandas as pd

from debtrank import calculate_debtrank


def run_monte_carlo(network, number_of_simulations=3000, seed=42):
    """Compare uniform random failures with failures weighted by bank size."""
    random_generator = np.random.default_rng(seed)
    bank_ids = list(network.nodes)
    asset_sizes = np.array([network.nodes[bank]["total_assets"] for bank in bank_ids])
    size_probabilities = asset_sizes / asset_sizes.sum()

    results = []
    for scenario, probabilities in [
        ("Random failure", None),
        ("Size-weighted failure", size_probabilities),
    ]:
        for simulation_number in range(1, number_of_simulations + 1):
            shocked_bank = random_generator.choice(bank_ids, p=probabilities)
            systemic_loss, _ = calculate_debtrank(network, shocked_bank)
            results.append(
                {
                    "scenario": scenario,
                    "simulation": simulation_number,
                    "shocked_bank": shocked_bank,
                    "systemic_loss": systemic_loss,
                }
            )

    return pd.DataFrame(results)


def summarise_results(simulation_results):
    """Calculate the three requested systemic-loss statistics for each scenario."""
    summary = simulation_results.groupby("scenario")["systemic_loss"].agg(
        mean="mean",
        median="median",
        percentile_95=lambda values: values.quantile(0.95),
    )
    return summary.reset_index()
