"""Interactive dashboard for exploring interbank contagion scenarios.

Run from the project root with:
    streamlit run app.py
"""

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import streamlit as st


# Make the reusable analysis code inside src/ available to this dashboard.
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from build_network import build_lending_network, save_edge_list
from debtrank import calculate_debtrank, rank_banks_by_systemic_impact
from generate_bank_data import create_bank_data
from monte_carlo import run_monte_carlo, summarise_results
from scenario_analysis import apply_core_capital_buffer, calculate_network_metrics


st.set_page_config(
    page_title="Interbank Systemic Risk Explorer",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .block-container { max-width: 1500px; padding-top: 2rem; padding-bottom: 3rem; }
    [data-testid="stMetric"] { background: #f4f7fb; border: 1px solid #d9e2ec; padding: 1rem; border-radius: 8px; }
    [data-testid="stMetricValue"] { font-size: 1.8rem; }
    h1 { color: #12304a; }
    h2, h3 { color: #1d4966; }
    </style>
    """,
    unsafe_allow_html=True,
)


def load_or_create_analysis():
    """Load saved results, or create them if this is the first dashboard run."""
    data_folder = PROJECT_ROOT / "data"
    output_folder = PROJECT_ROOT / "outputs"
    data_folder.mkdir(exist_ok=True)
    output_folder.mkdir(exist_ok=True)

    banks_path = data_folder / "banks.csv"
    edges_path = data_folder / "lending_network.csv"
    results_path = output_folder / "monte_carlo_results.csv"
    ranking_path = output_folder / "systemic_importance_ranking.csv"

    # Generate the two input files only if they do not already exist.
    if not banks_path.exists() or not edges_path.exists():
        banks = create_bank_data()
        banks.to_csv(banks_path, index=False)
        network = build_lending_network(banks)
        save_edge_list(network, edges_path)
    else:
        banks = pd.read_csv(banks_path)
        network = build_lending_network(banks)

    # Reuse saved Monte Carlo results, because 3,000 simulations take longer.
    if not results_path.exists():
        results = run_monte_carlo(network, number_of_simulations=3000)
        results.to_csv(results_path, index=False)
        summarise_results(results).to_csv(
            output_folder / "monte_carlo_summary.csv", index=False
        )
    else:
        results = pd.read_csv(results_path)

    if not ranking_path.exists():
        ranking = rank_banks_by_systemic_impact(network)
        ranking.to_csv(ranking_path, index=False)
    else:
        ranking = pd.read_csv(ranking_path)

    return banks, network, results, ranking


def draw_network(network, shocked_bank):
    """Draw the lending network and highlight the bank selected by the user."""
    positions = nx.spring_layout(network, seed=42, k=1.2)
    node_colors = []

    for bank in network.nodes:
        if bank == shocked_bank:
            node_colors.append("#f1c40f")  # Yellow means selected failure.
        elif network.nodes[bank]["bank_type"] == "Core":
            node_colors.append("#c0392b")  # Red means core bank.
        else:
            node_colors.append("#2980b9")  # Blue means peripheral bank.

    node_sizes = [network.nodes[bank]["total_assets"] / 5 for bank in network.nodes]

    figure, axis = plt.subplots(figsize=(10, 7))
    nx.draw_networkx_nodes(
        network, positions, node_color=node_colors, node_size=node_sizes, ax=axis
    )
    nx.draw_networkx_edges(
        network, positions, arrows=True, alpha=0.45, arrowsize=12, ax=axis
    )
    nx.draw_networkx_labels(network, positions, font_size=8, ax=axis)
    axis.set_title("Lending Network: Yellow = Selected Failed Bank")
    axis.axis("off")
    return figure


# Load the model data once for the current dashboard session.
banks, network, simulation_results, ranking = load_or_create_analysis()

st.title("Interbank Systemic Risk Explorer")
st.write(
    "Select a bank failure to see how financial distress travels through the "
    "synthetic interbank lending network."
)
st.info(
    "Start in the sidebar: choose a failing bank and adjust the shock assumptions. "
    "The metrics and affected-bank table update automatically."
)

st.sidebar.header("Shock Scenario")
selected_bank = st.sidebar.selectbox(
    "Bank that defaults", options=banks["bank_id"].tolist()
)
shock_severity = st.sidebar.slider(
    "Initial shock severity", min_value=0.10, max_value=1.00, value=1.00, step=0.05
)
loss_given_default = st.sidebar.slider(
    "Loss given default", min_value=0.10, max_value=1.00, value=1.00, step=0.05
)
capital_multiplier = st.sidebar.slider(
    "Core-bank capital buffer multiplier",
    min_value=1.00,
    max_value=2.00,
    value=1.00,
    step=0.05,
)

# Run DebtRank immediately when the selected bank changes.
systemic_impact, distress = calculate_debtrank(
    network, selected_bank, shock_severity, loss_given_default
)

# A policy scenario raises core capital while holding the lending network fixed.
policy_network = apply_core_capital_buffer(network, capital_multiplier)
policy_impact, _ = calculate_debtrank(
    policy_network, selected_bank, shock_severity, loss_given_default
)
impact_reduction = systemic_impact - policy_impact
selected_bank_details = banks.loc[banks["bank_id"] == selected_bank].iloc[0]

left_column, middle_column, right_column, policy_column = st.columns(4)
left_column.metric("Selected bank", selected_bank)
middle_column.metric("Bank type", selected_bank_details["bank_type"])
right_column.metric("Systemic impact", f"{systemic_impact:.2%}")
policy_column.metric(
    "Impact after capital policy",
    f"{policy_impact:.2%}",
    delta=f"{-impact_reduction:.2%}",
    delta_color="inverse",
)

st.caption(
    "Systemic impact is the share of total banking-system assets affected by distress."
)

# Let the user download the exact scenario configured in the sidebar.
scenario_report = pd.DataFrame(
    [
        {
            "selected_bank": selected_bank,
            "shock_severity": shock_severity,
            "loss_given_default": loss_given_default,
            "core_capital_multiplier": capital_multiplier,
            "base_systemic_impact": systemic_impact,
            "policy_systemic_impact": policy_impact,
            "impact_reduction": impact_reduction,
        }
    ]
)
st.download_button(
    "Download selected scenario report (CSV)",
    data=scenario_report.to_csv(index=False).encode("utf-8"),
    file_name="selected_stress_test_scenario.csv",
    mime="text/csv",
)

scenario_tab, comparison_tab, ranking_tab = st.tabs(
    ["Selected Failure", "Monte Carlo Comparison", "Systemic Importance"]
)

with scenario_tab:
    network_column, table_column = st.columns([3, 2])

    with network_column:
        st.subheader("How distress travels through the network")
        st.caption(
            "Yellow = selected failed bank | Red = core bank | Blue = peripheral bank"
        )
        st.pyplot(
            draw_network(network, selected_bank),
            clear_figure=True,
            use_container_width=True,
        )

    with table_column:
        # Convert the distress dictionary into a table for the selected scenario.
        distress_table = pd.DataFrame(
            {"bank_id": list(distress.keys()), "distress": list(distress.values())}
        )
        distress_table = distress_table.merge(
            banks[["bank_id", "bank_type", "total_assets", "capital"]], on="bank_id"
        )
        affected_banks = distress_table.loc[distress_table["distress"] > 0].copy()
        affected_banks["distress"] = affected_banks["distress"].map("{:.2%}".format)
        affected_banks = affected_banks.sort_values("total_assets", ascending=False)

        st.subheader("Banks Affected by Distress")
        st.dataframe(affected_banks, hide_index=True, use_container_width=True)

with comparison_tab:
    summary = summarise_results(simulation_results)
    st.subheader("Monte Carlo Loss Summary")
    st.caption(
        "Each distribution shows the share of total banking-system assets affected "
        "across 3,000 simulated failures."
    )
    st.dataframe(summary, hide_index=True, use_container_width=True)

    figure, axis = plt.subplots(figsize=(10, 5))
    for scenario, color in [
        ("Random failure", "#2980b9"),
        ("Size-weighted failure", "#c0392b"),
    ]:
        losses = simulation_results.loc[
            simulation_results["scenario"] == scenario, "systemic_loss"
        ]
        axis.hist(losses, bins=20, alpha=0.55, label=scenario, color=color)

    axis.set_xlabel("Systemic loss (share of total assets)")
    axis.set_ylabel("Number of simulations")
    axis.legend()
    st.pyplot(figure, clear_figure=True, use_container_width=True)

with ranking_tab:
    st.subheader("Banks Ranked by Individual Failure Impact")
    ranking_for_display = ranking.copy()
    ranking_for_display["systemic_impact"] = ranking_for_display["systemic_impact"].map(
        "{:.2%}".format
    )
    st.dataframe(ranking_for_display, hide_index=True, use_container_width=True)

    st.subheader("Network Exposure Metrics")
    network_metrics = calculate_network_metrics(network)
    network_metrics["capital_ratio"] = network_metrics["capital_ratio"].map(
        "{:.2%}".format
    )
    st.dataframe(network_metrics, hide_index=True, use_container_width=True)
