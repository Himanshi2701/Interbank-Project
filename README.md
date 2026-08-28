m# Interbank Contagion & Systemic Risk Analysis

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
6. Explore user-selected stress tests in an interactive dashboard, including
   shock severity, loss-given-default, and core-bank capital-buffer scenarios.

## Key Finding

In the baseline simulation, random failures produce a mean systemic loss of
9.14%, while size-weighted failures produce a mean loss of 20.22%. This shows
that failures involving large, well-connected core banks create greater
contagion in the synthetic system.

## Project Structure

```text
interbank-project/
|-- app.py       # Interactive Streamlit stress-testing dashboard
|-- data/        # Generated bank and lending-network CSV files
|-- notebooks/   # End-to-end Jupyter analysis notebook
|-- outputs/     # Simulation results, rankings, and plots
|-- src/         # Clear, reusable Python analysis modules
|-- README.md
`-- requirements.txt
```

## Tools Used

- Python
- pandas
- NumPy
- NetworkX
- Matplotlib
- Jupyter Notebook
- Streamlit

## Run the Project

Install dependencies and run the full pipeline from the project root:

```powershell
pip install -r requirements.txt
python src/run_analysis.py
```

The generated figures and CSV files will appear in `outputs/`.

## Interactive Dashboard

The Streamlit dashboard lets a user select a bank failure and immediately see
the resulting DebtRank systemic impact, affected banks, lending network, and
Monte Carlo comparison. It also tests recovery assumptions and whether higher
core-bank capital buffers reduce contagion. Run it from the project root:

```powershell
streamlit run app.py
```
## Live Dashboard

[Open the Interbank Systemic Risk Explorer](https://interbank-project-2701.streamlit.app)
