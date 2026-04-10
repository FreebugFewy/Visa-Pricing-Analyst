# Visa Pricing Analyst

This project models the pricing strategy analytics work performed by Visa's Global Pricing Strategy team. It synthesises 2,160 rows of transaction data across 5 regions, 6 merchant categories, and 3 card types to surface interchange rate trends, merchant acceptance patterns, and deal P&L economics. The centrepiece is an interactive deal simulator that models the net revenue, NPV, and break-even volume of a merchant acceptance deal — the same kind of tool a Pricing Strategy Analyst uses to evaluate and structure client deals.

## Live Dashboard

**URL:** https://visa-pricing-analyst-eahxvbuodqjhohv4pikbct.streamlit.app/

## Job Posting

- **Role:** Analyst, Pricing Strategy
- **Company:** Visa Inc.

This project directly demonstrates the role's core requirements: rigorous quantitative analysis, financial modeling, and the ability to synthesise large datasets into actionable pricing recommendations for business leaders.

## Tech Stack

| Layer | Tool |
|---|---|
| Data | Synthesized CSV — Python generator script |
| Data Processing | Pandas |
| Financial Model | Python pure function (`compute_deal_pnl`) |
| Visualisation | Altair |
| Dashboard | Streamlit (two-page multipage app) |
| Testing | pytest (8 unit tests) |
| Deployment | Streamlit Community Cloud |

## Pipeline Diagram

```mermaid
flowchart TD
    CSV[("visa_pricing_metrics.csv\n2,160 rows")]

    CSV -->|"@st.cache_data"| P1["app.py\n📊 Market Overview\nKPI cards · Volume trend\nInterchange · Acceptance · Revenue"]
    CSV -->|"@st.cache_data"| P2["pages/2_deal_simulator.py\n🤝 Deal Simulator"]

    P2 --> INPUTS["User Inputs\nMerchant · Category · Region\nVolume · Discount · Growth · Term"]
    INPUTS --> FN["compute_deal_pnl()\nutils/deal_pnl.py\nPure function — no Streamlit dependency"]
    FN --> OUT1["KPI Cards\nNet Revenue · NPV · Break-even uplift"]
    FN --> OUT2["Year-by-Year P&L Table"]
    FN --> OUT3["Gross vs Net Revenue Bar Chart"]
    FN --> OUT4["Verdict Banner\nFavorable · Conditional · Requires Approval"]

    P2 -->|"derives baseline\ninterchange rate"| CSV
```

## Data Schema

The dataset (`streamlit_app/data/visa_pricing_metrics.csv`) has 2,160 rows — one per month/region/category/card-type combination.

| Column | Type | Description |
|---|---|---|
| `month` | date | Month of observation (Jan 2024 – Dec 2025) |
| `region` | string | One of 5 global regions |
| `merchant_category` | string | One of 6 merchant categories |
| `card_type` | string | Credit, Debit, or Prepaid |
| `transaction_volume` | integer | Number of transactions |
| `avg_transaction_usd` | float | Average transaction value in USD |
| `interchange_rate` | float | Interchange rate as a decimal (e.g. 0.0195) |
| `revenue_usd` | float | Revenue = volume × avg_txn × interchange_rate |
| `acceptance_rate` | float | Share of attempted transactions approved |

## Dashboard Preview

### Market Overview
![Market Overview](docs/market-overview.png)

### Deal Simulator
![Deal Simulator](docs/deal-simulator.png)

## Key Insights

**Descriptive (what does the data show?):** E-commerce and Travel carry the highest interchange rates at 2.4% and 2.2% respectively, while Fuel sits at 1.45% — a 66% spread across categories that represents significant revenue variation per transaction.

**Diagnostic (why does the gap exist?):** North America leads merchant acceptance at 96% while Middle East & Africa sits at 83%, a 13-point gap that persists across all merchant categories — pointing to network maturity and infrastructure differences rather than category-specific friction.

**Recommendation:** Target E-commerce deal negotiations with volume-for-discount structures first — the combination of high interchange headroom (2.4%) and strong digital growth trajectory means larger deals can absorb meaningful discounts while remaining NPV-positive. Use the Deal Simulator to model the exact break-even volume before committing to a discount tier.

## Setup & Reproduction

**Requirements:** Python 3.10+

```bash
# Install dependencies
pip install streamlit altair pandas pytest

# Run the dashboard (from streamlit_app/)
cd streamlit_app
streamlit run app.py

# Run tests (from project root)
pytest
```

To regenerate the dataset from scratch:

```bash
cd streamlit_app
python generate_data.py
```

## Repository Structure

    .
    ├── streamlit_app/
    │   ├── app.py                   # Page 1: Market Overview dashboard
    │   ├── pages/
    │   │   └── 2_deal_simulator.py  # Page 2: Deal Simulator
    │   ├── utils/
    │   │   ├── data_loader.py       # Shared cached CSV loader
    │   │   └── deal_pnl.py          # Core financial model (pure function)
    │   ├── data/
    │   │   └── visa_pricing_metrics.csv
    │   └── generate_data.py         # Synthetic data generator
    ├── tests/
    │   └── test_deal_pnl.py         # 8 unit tests for the financial model
    ├── docs/
    │   ├── proposal.md              # Project proposal
    │   └── pipeline-diagram.md      # Data flow diagram
    ├── pytest.ini                   # Test configuration
    └── README.md
