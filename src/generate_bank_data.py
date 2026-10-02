"""Create a small, reproducible synthetic banking dataset."""

from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_FOLDER = PROJECT_ROOT / "data"
REQUIRED_COLUMNS = ["bank_id", "bank_type", "total_assets", "capital"]


def validate_bank_data(banks):
    """Ensure the generated bank table is complete and internally consistent."""
    if banks is None or banks.empty:
        raise ValueError("Bank table is empty or missing.")

    missing_columns = [column for column in REQUIRED_COLUMNS if column not in banks.columns]
    if missing_columns:
        raise ValueError(f"Bank table is missing required columns: {missing_columns}")

    if banks.duplicated(subset=["bank_id"]).any():
        raise ValueError("Bank IDs must be unique.")

    if banks.isna().any().any():
        raise ValueError("Bank table contains missing values.")

    if not set(banks["bank_type"].unique()).issubset({"Core", "Periphery"}):
        raise ValueError("Bank types must be limited to 'Core' and 'Periphery'.")

    if len(banks.loc[banks["bank_type"] == "Core"]) != 5:
        raise ValueError("The synthetic system must include exactly five core banks.")

    if len(banks.loc[banks["bank_type"] == "Periphery"]) != 15:
        raise ValueError("The synthetic system must include exactly fifteen peripheral banks.")

    if (banks["total_assets"] <= 0).any():
        raise ValueError("All bank assets must be positive.")

    if (banks["capital"] <= 0).any():
        raise ValueError("All bank capital must be positive.")

    capital_ratio = banks["capital"] / banks["total_assets"]
    if (capital_ratio <= 0.05).any() or (capital_ratio >= 0.25).any():
        raise ValueError("Capital ratios must remain between 5% and 25% for realism.")

    return banks


def create_bank_data(seed=42):
    """Return a table containing five core banks and fifteen peripheral banks."""
    random_generator = np.random.default_rng(seed)

    bank_rows = []

    # Core banks are deliberately much larger than peripheral banks.
    for number in range(1, 6):
        assets = int(random_generator.integers(8_000, 15_001))
        bank_rows.append(
            {
                "bank_id": f"Bank_{number:02d}",
                "bank_type": "Core",
                "total_assets": assets,
                # Capital is the bank's loss-absorbing safety cushion.
                "capital": round(assets * 0.10, 2),
            }
        )

    for number in range(6, 21):
        assets = int(random_generator.integers(500, 2_001))
        bank_rows.append(
            {
                "bank_id": f"Bank_{number:02d}",
                "bank_type": "Periphery",
                "total_assets": assets,
                "capital": round(assets * 0.10, 2),
            }
        )

    banks = pd.DataFrame(bank_rows)
    return validate_bank_data(banks)


def main():
    DATA_FOLDER.mkdir(exist_ok=True)
    banks = create_bank_data()
    output_path = DATA_FOLDER / "banks.csv"
    banks.to_csv(output_path, index=False)

    print(f"Saved {len(banks)} banks to: {output_path}")
    print("\nFirst five rows:")
    print(banks.head())
    print("\nTotals by bank type:")
    print(banks.groupby("bank_type")[["total_assets", "capital"]].sum())


if __name__ == "__main__":
    main()
