import os
import sys

import pandas as pd

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

SRC_ROOT = os.path.join(PROJECT_ROOT, "src")
if SRC_ROOT not in sys.path:
    sys.path.insert(0, SRC_ROOT)

from build_network import build_lending_network
from debtrank import calculate_debtrank
from generate_bank_data import create_bank_data
from monte_carlo import run_monte_carlo, summarise_results
from scenario_analysis import apply_core_capital_buffer


def test_bank_failure_has_bounded_systemic_impact():
    banks = create_bank_data()
    network = build_lending_network(banks)

    impact, distress = calculate_debtrank(network, "Bank_01")

    assert 0.0 <= impact <= 1.0
    assert distress["Bank_01"] == 1.0
    assert all(value >= 0 for value in distress.values())


def test_capital_buffer_reduces_contagion():
    banks = create_bank_data()
    network = build_lending_network(banks)
    buffered_network = apply_core_capital_buffer(network, 1.5)

    base_impact, _ = calculate_debtrank(network, "Bank_01")
    buffered_impact, _ = calculate_debtrank(buffered_network, "Bank_01")

    assert buffered_impact <= base_impact


def test_monte_carlo_summary_is_valid():
    banks = create_bank_data()
    network = build_lending_network(banks)
    results = run_monte_carlo(network, number_of_simulations=50, seed=123)
    summary = summarise_results(results)

    assert list(summary["scenario"].unique()) == ["Random failure", "Size-weighted failure"]
    assert set(summary.columns) >= {"scenario", "mean", "median", "percentile_95"}
    assert len(results) == 100
    assert all(pd.notna(results["systemic_loss"]))


if __name__ == "__main__":
    import pytest

    raise SystemExit(pytest.main([__file__]))
