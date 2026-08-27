"""Create a small, reproducible synthetic banking dataset."""

from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_FOLDER = PROJECT_ROOT / "data"


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

    return pd.DataFrame(bank_rows)


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
