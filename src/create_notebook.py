"""Create the project notebook using the same readable analysis functions."""

from pathlib import Path

import nbformat as nbf


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def markdown(text):
    """Make a Markdown notebook cell."""
    return nbf.v4.new_markdown_cell(text)


def code(text):
    """Make a Python notebook cell."""
    return nbf.v4.new_code_cell(text)


def main():
    notebook = nbf.v4.new_notebook()
    notebook["cells"] = [
        markdown(
            "# Interbank Contagion & Systemic Risk Analysis\n"
            "This notebook builds a small synthetic banking system, models interbank "
            "lending, measures contagion with a simple DebtRank model, and compares "
            "failure scenarios using Monte Carlo simulation."
        ),
        markdown("## Setup\nImport the project functions and set the project paths."),
        code(
            "from pathlib import Path\n"
            "import sys\n"
            "import matplotlib.pyplot as plt\n"
            "import pandas as pd\n\n"
            "# The notebook is in notebooks/, so its parent is the project root.\n"
            "PROJECT_ROOT = Path.cwd().resolve()\n"
            "if not (PROJECT_ROOT / 'src').exists():\n"
            "    PROJECT_ROOT = PROJECT_ROOT.parent\n\n"
            "sys.path.insert(0, str(PROJECT_ROOT / 'src'))\n\n"
            "from build_network import build_lending_network, save_edge_list\n"
            "from create_plots import create_all_plots\n"
            "from debtrank import calculate_debtrank, rank_banks_by_systemic_impact\n"
            "from generate_bank_data import create_bank_data\n"
            "from monte_carlo import run_monte_carlo, summarise_results"
        ),
        markdown(
            "## Step 1: Synthetic bank data\n"
            "We create five large core banks and fifteen smaller peripheral banks. "
            "Capital is each bank's initial loss-absorbing cushion."
        ),
        code(
            "banks = create_bank_data()\n"
            "banks.to_csv(PROJECT_ROOT / 'data' / 'banks.csv', index=False)\n"
            "banks"
        ),
        markdown(
            "## Step 2: Lending network\n"
            "An arrow from A to B means A lends to B. Core banks lend to one another, "
            "while peripheral banks borrow from one or two core banks."
        ),
        code(
            "network = build_lending_network(banks)\n"
            "save_edge_list(network, PROJECT_ROOT / 'data' / 'lending_network.csv')\n"
            "print(f'Banks: {network.number_of_nodes()}')\n"
            "print(f'Lending relationships: {network.number_of_edges()}')"
        ),
        markdown(
            "## Step 3: DebtRank contagion\n"
            "We default one bank. Its lenders lose the relevant exposure relative to "
            "their capital, which can cause further distress. The final score is the "
            "share of system assets affected by distress."
        ),
        code(
            "example_bank = 'Bank_01'\n"
            "impact, distress = calculate_debtrank(network, example_bank)\n"
            "print(f'Systemic impact of {example_bank}: {impact:.2%}')\n"
            "pd.DataFrame({'bank_id': distress.keys(), 'distress': distress.values()}).sort_values('distress', ascending=False)"
        ),
        code(
            "ranking = rank_banks_by_systemic_impact(network)\n"
            "ranking.to_csv(PROJECT_ROOT / 'outputs' / 'systemic_importance_ranking.csv', index=False)\n"
            "ranking.head(10)"
        ),
        markdown(
            "## Step 4: Monte Carlo simulation\n"
            "We repeat the shock experiment 3,000 times. Random failure gives every "
            "bank the same chance of failure; size-weighted failure makes large banks "
            "more likely to fail."
        ),
        code(
            "results = run_monte_carlo(network, number_of_simulations=3000)\n"
            "results.to_csv(PROJECT_ROOT / 'outputs' / 'monte_carlo_results.csv', index=False)\n"
            "summary = summarise_results(results)\n"
            "summary.to_csv(PROJECT_ROOT / 'outputs' / 'monte_carlo_summary.csv', index=False)\n"
            "summary"
        ),
        markdown(
            "## Step 5: Visualisations\n"
            "The figures show the lending network, the two loss distributions, and "
            "the ten banks with the greatest systemic impact."
        ),
        code(
            "plot_paths = create_all_plots(network, results, ranking, PROJECT_ROOT / 'outputs')\n"
            "for path in plot_paths.values():\n"
            "    image = plt.imread(path)\n"
            "    plt.figure(figsize=(10, 6))\n"
            "    plt.imshow(image)\n"
            "    plt.axis('off')\n"
            "    plt.show()"
        ),
        markdown(
            "## Conclusion\n"
            "Compare the random and size-weighted summary statistics above. In this "
            "synthetic system, failures that are more likely to involve large core "
            "banks should create larger systemic losses."
        ),
    ]
    notebook["metadata"] = {
        "kernelspec": {
            "display_name": "Python 3.14 (Interbank Project)",
            "language": "python",
            "name": "interbank-project",
        },
        "language_info": {"name": "python", "version": "3.14"},
    }

    output_path = PROJECT_ROOT / "notebooks" / "main_analysis.ipynb"
    nbf.write(notebook, output_path)
    print(f"Created notebook: {output_path}")


if __name__ == "__main__":
    main()
