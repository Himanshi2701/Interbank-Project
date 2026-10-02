import os
import sys
import unittest

import pandas as pd

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

SRC_ROOT = os.path.join(PROJECT_ROOT, "src")
if SRC_ROOT not in sys.path:
    sys.path.insert(0, SRC_ROOT)

from build_network import build_lending_network
from generate_bank_data import create_bank_data


class DataQualityTests(unittest.TestCase):
    def test_bank_data_is_complete_and_realistic(self):
        banks = create_bank_data()

        self.assertFalse(banks.isna().any().any())
        self.assertTrue((banks["total_assets"] > 0).all())
        self.assertTrue((banks["capital"] > 0).all())
        self.assertSetEqual(set(banks["bank_type"].unique()), {"Core", "Periphery"})
        self.assertGreater((banks["capital"] / banks["total_assets"]).min(), 0.05)
        self.assertLess((banks["capital"] / banks["total_assets"]).max(), 0.25)

    def test_lending_network_has_positive_non_missing_exposures(self):
        banks = create_bank_data()
        network = build_lending_network(banks)

        self.assertGreater(network.number_of_nodes(), 0)
        self.assertGreater(network.number_of_edges(), 0)
        self.assertFalse(any(u == v for u, v in network.edges()))

        exposure_values = [
            data["exposure"] for _, _, data in network.edges(data=True)
        ]
        self.assertTrue(all(value > 0 for value in exposure_values))
        self.assertFalse(any(pd.isna(value) for value in exposure_values))

    def test_invalid_bank_data_is_rejected_before_network_build(self):
        invalid_banks = pd.DataFrame(
            [
                {
                    "bank_id": "Bank_01",
                    "bank_type": "Core",
                    "total_assets": 1000,
                    "capital": None,
                },
                {
                    "bank_id": "Bank_02",
                    "bank_type": "Periphery",
                    "total_assets": 500,
                    "capital": 50,
                },
            ]
        )

        with self.assertRaises(ValueError):
            build_lending_network(invalid_banks)


if __name__ == "__main__":
    unittest.main()
