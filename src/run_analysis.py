"""Run the full Interbank Contagion and Systemic Risk Analysis pipeline."""

from pathlib import Path
import sys

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from build_network import build_lending_network, save_edge_list
from create_plots import create_all_plots
from debtrank import rank_banks_by_systemic_impact
from generate_bank_data import create_bank_data
from monte_carlo import run_monte_carlo, summarise_results


def main():
    data_folder = PROJECT_ROOT / "data"
    output_folder = PROJECT_ROOT / "outputs"
    data_folder.mkdir(exist_ok=True)
    output_folder.mkdir(exist_ok=True)

    # Step 1: Create and save the synthetic bank table.
    banks = create_bank_data()
    banks.to_csv(data_folder / "banks.csv", index=False)

    # Step 2: Create and save the directed lending network.
    network = build_lending_network(banks)
    save_edge_list(network, data_folder / "lending_network.csv")

    # Step 3: Find the systemic impact caused by each individual bank failure.
    ranking = rank_banks_by_systemic_impact(network)
    ranking.to_csv(output_folder / "systemic_importance_ranking.csv", index=False)

    # Step 4: Run the two Monte Carlo failure scenarios.
    results = run_monte_carlo(network, number_of_simulations=3000)
    results.to_csv(output_folder / "monte_carlo_results.csv", index=False)
    results.loc[results["scenario"] == "Random failure"].to_csv(
        output_folder / "random_failure_results.csv", index=False
    )
    results.loc[results["scenario"] == "Size-weighted failure"].to_csv(
        output_folder / "size_weighted_failure_results.csv", index=False
    )
    summary = summarise_results(results)
    summary.to_csv(output_folder / "monte_carlo_summary.csv", index=False)

    # Step 5: Create figures from the analysis results.
    plot_paths = create_all_plots(network, results, ranking, output_folder)

    print("Analysis completed successfully.\n")
    print("Monte Carlo summary (systemic loss is a share of total assets):")
    print(summary.to_string(index=False))
    print("\nTop 10 systemically important banks:")
    print(ranking.head(10).to_string(index=False))
    print("\nCreated plots:")
    for path in plot_paths.values():
        print(path)


if __name__ == "__main__":
    main()
