# Interbank Contagion & Systemic Risk Analysis

## Objective

This project models how the failure of one bank can spread financial distress
through an interbank lending network. It is a small, synthetic example built
to demonstrate network analysis, systemic-risk modelling, and Monte Carlo
simulation in Python.

## Method

1. Generate 20 synthetic banks: five large core banks and fifteen smaller
   peripheral banks.
2. Build a directed lending network. An edge `A -> B` means bank A lends to
   bank B.
3. Apply a simple DebtRank-style contagion model. When a borrower is
   distressed, lenders lose a fraction of their capital equal to their
   exposure to that borrower.
4. Rank banks by the systemic impact of their individual failure.
5. Run 3,000 Monte Carlo simulations under random and size-weighted bank
   failure scenarios.

## Key Finding

Placeholder: compare the mean and 95th-percentile systemic loss for random
and size-weighted failures after running the analysis. In this model,
size-weighted failures are expected to produce larger losses because core
banks hold a larger share of system assets and lending relationships.

## Project Structure

```text
interbank-project/
├── data/       # Generated bank and lending-network CSV files
├── notebooks/  # End-to-end Jupyter analysis notebook
├── outputs/    # Simulation results, rankings, and plots
├── src/        # Clear, reusable Python analysis modules
├── README.md
└── requirements.txt
```

## Tools Used

- Python
- pandas
- NumPy
- NetworkX
- Matplotlib
- Jupyter Notebook

## Run the Project

Install dependencies and run the full pipeline from the project root:

```powershell
pip install -r requirements.txt
python src/run_analysis.py
```

The generated figures and CSV files will appear in `outputs/`.
