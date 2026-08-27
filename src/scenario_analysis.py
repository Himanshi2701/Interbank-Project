"""Simple stress-testing helpers used by the interactive dashboard."""

import pandas as pd


def apply_core_capital_buffer(network, capital_multiplier):
    """Return a copy of the network with higher capital at every core bank.

    For example, 1.25 represents a 25% increase in core-bank capital. Lending
    exposures stay fixed, so this isolates the effect of bigger capital buffers.
    """
    scenario_network = network.copy()

    for bank in scenario_network.nodes:
        if scenario_network.nodes[bank]["bank_type"] == "Core":
            original_capital = scenario_network.nodes[bank]["capital"]
            scenario_network.nodes[bank]["capital"] = (
                original_capital * capital_multiplier
            )

    return scenario_network


def calculate_network_metrics(network):
    """Create useful relationship and exposure metrics for every bank."""
    metric_rows = []

    for bank in network.nodes:
        # Outgoing edges are loans made by this bank to its borrowers.
        total_lending = sum(
            network[bank][borrower]["exposure"]
            for borrower in network.successors(bank)
        )

        # Incoming edges are loans received by this bank from its lenders.
        total_borrowing = sum(
            network[lender][bank]["exposure"] for lender in network.predecessors(bank)
        )

        total_assets = network.nodes[bank]["total_assets"]
        capital = network.nodes[bank]["capital"]
        metric_rows.append(
            {
                "bank_id": bank,
                "bank_type": network.nodes[bank]["bank_type"],
                "number_of_borrowers": network.out_degree(bank),
                "number_of_lenders": network.in_degree(bank),
                "total_lending": round(total_lending, 2),
                "total_borrowing": round(total_borrowing, 2),
                "capital_ratio": round(capital / total_assets, 4),
            }
        )

    return pd.DataFrame(metric_rows).sort_values("total_lending", ascending=False)
