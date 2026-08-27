"""Create the three figures used in the project report and notebook."""

from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx


def create_network_plot(network, output_path):
    """Draw core banks in red and peripheral banks in blue."""
    positions = nx.spring_layout(network, seed=42)
    node_colors = [
        "#c0392b" if network.nodes[bank]["bank_type"] == "Core" else "#2980b9"
        for bank in network.nodes
    ]
    node_sizes = [network.nodes[bank]["total_assets"] / 3 for bank in network.nodes]

    plt.figure(figsize=(11, 8))
    nx.draw_networkx_nodes(network, positions, node_color=node_colors, node_size=node_sizes)
    nx.draw_networkx_edges(network, positions, arrows=True, alpha=0.45, arrowsize=12)
    nx.draw_networkx_labels(network, positions, font_size=8, font_color="black")
    plt.title("Synthetic Interbank Lending Network\nRed: Core banks | Blue: Peripheral banks")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()


def create_histogram(simulation_results, output_path):
    """Compare loss distributions for the two simulation scenarios."""
    plt.figure(figsize=(10, 6))
    for scenario, color in [("Random failure", "#2980b9"), ("Size-weighted failure", "#c0392b")]:
        losses = simulation_results.loc[
            simulation_results["scenario"] == scenario, "systemic_loss"
        ]
        plt.hist(losses, bins=20, alpha=0.55, label=scenario, color=color)

    plt.title("Distribution of Systemic Losses")
    plt.xlabel("Systemic loss (share of total banking assets)")
    plt.ylabel("Number of simulations")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def create_importance_bar_chart(ranking, output_path):
    """Plot the ten banks with the greatest DebtRank impact."""
    top_ten = ranking.head(10).sort_values("systemic_impact")
    plt.figure(figsize=(10, 6))
    plt.barh(top_ten["bank_id"], top_ten["systemic_impact"], color="#8e44ad")
    plt.title("Top 10 Systemically Important Banks")
    plt.xlabel("Systemic impact score")
    plt.ylabel("Bank")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def create_all_plots(network, simulation_results, ranking, output_folder):
    """Create all output figures and return their paths."""
    output_folder = Path(output_folder)
    output_folder.mkdir(exist_ok=True)
    paths = {
        "network": output_folder / "lending_network.png",
        "histogram": output_folder / "systemic_loss_histogram.png",
        "importance": output_folder / "systemic_importance_top_10.png",
    }
    create_network_plot(network, paths["network"])
    create_histogram(simulation_results, paths["histogram"])
    create_importance_bar_chart(ranking, paths["importance"])
    return paths
