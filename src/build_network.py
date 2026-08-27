"""Build and save a simple directed interbank lending network."""

from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_FOLDER = PROJECT_ROOT / "data"


def build_lending_network(banks, seed=42):
    """Create a directed graph where lender -> borrower.

    A core bank lends to every other core bank.  Each peripheral bank borrows
    from one or two core banks.  The edge attribute 'exposure' is the amount
    that the lender would lose if the borrower fully defaults.
    """
    random_generator = np.random.default_rng(seed)
    network = nx.DiGraph()

    # Store the bank table values on graph nodes for later analysis and plots.
    for _, bank in banks.iterrows():
        network.add_node(
            bank["bank_id"],
            bank_type=bank["bank_type"],
            total_assets=float(bank["total_assets"]),
            capital=float(bank["capital"]),
        )

    core_banks = banks.loc[banks["bank_type"] == "Core", "bank_id"].tolist()
    peripheral_banks = banks.loc[
        banks["bank_type"] == "Periphery", "bank_id"
    ].tolist()
    capital_by_bank = banks.set_index("bank_id")["capital"].to_dict()

    # Every core bank lends to each of the other core banks.
    for lender in core_banks:
        for borrower in core_banks:
            if lender != borrower:
                exposure = round(float(capital_by_bank[lender]) * 0.12, 2)
                network.add_edge(lender, borrower, exposure=exposure)

    # A peripheral bank borrows from one or two randomly selected core banks.
    for borrower in peripheral_banks:
        number_of_lenders = int(random_generator.integers(1, 3))
        lenders = random_generator.choice(
            core_banks, size=number_of_lenders, replace=False
        )
        for lender in lenders:
            exposure = round(float(capital_by_bank[lender]) * 0.04, 2)
            network.add_edge(lender, borrower, exposure=exposure)

    return network


def save_edge_list(network, output_path):
    """Save the NetworkX edges in a beginner-friendly CSV format."""
    edge_rows = []
    for lender, borrower, edge_data in network.edges(data=True):
        edge_rows.append(
            {
                "lender": lender,
                "borrower": borrower,
                "exposure": edge_data["exposure"],
            }
        )
    pd.DataFrame(edge_rows).to_csv(output_path, index=False)


def main():
    banks = pd.read_csv(DATA_FOLDER / "banks.csv")
    network = build_lending_network(banks)
    output_path = DATA_FOLDER / "lending_network.csv"
    save_edge_list(network, output_path)

    print(f"Saved {network.number_of_edges()} lending relationships to: {output_path}")
    print("\nNetwork convention: lender -> borrower")
    print(pd.read_csv(output_path).head())


if __name__ == "__main__":
    main()
