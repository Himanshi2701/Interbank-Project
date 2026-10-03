# Interbank Contagion & Systemic Risk Analysis

## Live Dashboard

Explore the model interactively: choose a bank failure, change the shock
assumptions, inspect the network, and compare the result with Monte Carlo
stress tests.

**[Open the live Interbank Systemic Risk Explorer](https://interbank-project-2701.streamlit.app/)**

> The live dashboard is hosted by Streamlit. GitHub stores the code and data,
> but it does not run Streamlit applications inside the repository page.

## What This Project Does

This project studies how a shock to one bank can propagate through a stylised
interbank lending network. It is a mathematical and computational modelling
project focused on:

> The model uses synthetic data and simplified assumptions. It is designed to
> illustrate contagion dynamics and systemic risk in a financial network, not to
> reproduce any specific real bank or regulatory stress-test framework.

- network analysis and graph theory,
- contagion and systemic risk,
- Monte Carlo simulation,
- sensitivity analysis,
- and reproducible data analysis in Python.

It is intentionally a small synthetic model. The goal is to show how a simple
financial network can be analysed in a clean, interpretable way without
building an AI system or a large production platform.

## Why This Fits an Applied Mathematics Profile

This project is well suited for an MSc in applied mathematics because it brings
together several core skills:

- probability and simulation,
- statistics and risk summarisation,
- linear algebra and network structure,
- computational thinking in Python,
- and interpretation of model outputs.

It is a good example of applied mathematical modelling rather than an AI-heavy
application. There is no RAG pipeline, no LLM workflow, and no generative-AI
component because the task is not to build one.

## Analysis Workflow

1. Generate 20 synthetic banks: five large core banks and fifteen smaller
   peripheral banks.
2. Build a directed lending network. An edge `A -> B` means bank A lends to
   bank B.
3. Apply a simple DebtRank-style contagion model. When a borrower is
   distressed, lenders lose a fraction of their capital equal to their
   exposure to that borrower.
4. Rank banks by the systemic impact of their individual failure.
5. Run Monte Carlo simulations under random and size-weighted bank failure
   scenarios.
6. Explore stress tests with different shock assumptions and core-bank capital
   buffers.

## Key Finding

In the baseline simulation, random failures produce a mean systemic loss of
around 9%, while size-weighted failures produce a larger mean loss. This shows
that failures involving large, well-connected banks create substantially more
contagion in the synthetic system.

## Project Structure

```text
interbank-project/
|-- app.py       # Interactive Streamlit stress-testing dashboard
|-- data/        # Generated bank and lending-network CSV files
|-- notebooks/   # End-to-end Jupyter analysis notebook
|-- outputs/     # Simulation results, rankings, and plots
|-- src/         # Core model and analysis modules
|-- tests/       # Data quality and model validation checks
|-- README.md
|-- requirements.txt
`-- run_dashboard.bat
```

## Skills Demonstrated

- Python for numerical and data analysis
- pandas and NumPy for data handling and simulation
- NetworkX for graph-based financial modelling
- statistics for scenario comparison and summarisation
- Monte Carlo methods for stress testing
- reproducible workflow design and reporting
- dashboard development for interactive exploration

## Run the Project

Install dependencies and run the analysis from the project root:

```powershell
pip install -r requirements.txt
python src/run_analysis.py
```

The generated figures and CSV files will appear in `outputs/`.

On Windows, double-click `run_dashboard.bat` to open the dashboard in your
browser. It starts Streamlit from the project folder, so no path configuration
is needed.

## Interactive Dashboard

The Streamlit dashboard lets a user select a bank failure and immediately see
its systemic impact, the affected banks, the network structure, and the Monte
Carlo comparison. It also tests how higher core-bank capital buffers reduce
contagion.

Run it from the project root:

```powershell
streamlit run app.py
```

The dashboard includes a **Refresh analysis data** button so saved outputs can
be regenerated if the model or synthetic data changes.

## Portfolio Positioning

This is best presented as a financial network analysis and simulation project in
applied mathematics, not as an AI or LLM project. It is a strong example of
computational modelling, statistical stress testing, and graph-based analysis.
It is well suited for a mathematical or quantitative portfolio and shows solid
technical depth without pretending to be something more advanced than it is.

The project is intentionally synthetic and educational. It reflects the general
mechanisms behind systemic risk in interbank markets, but it does not claim to
be a calibrated or real-world banking model.

## Role Relevance

This project is versatile enough to be discussed in several professional
contexts:

- Data Science: building a reproducible analysis pipeline, running simulations,
  and deriving evidence-based conclusions from data.
- Data Analysis: cleaning and validating datasets, checking assumptions, and
  turning results into business-facing insights.
- Consulting: framing a banking risk problem, comparing scenarios, and giving
  decision-ready recommendations.
- Management / Strategy: understanding systemic risk, capital buffers, and the
  business impact of failures in a networked system.
- Banking / Risk Roles: demonstrating awareness of contagion, exposure,
  capital adequacy, and stress testing in a simplified financial setting.

This makes the project realistic for a candidate applying to analytics,
quantitative, operations, strategy, or banking-related roles, while still
keeping the scope honest and technically grounded.
