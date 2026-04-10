import pandas as pd


def compute_deal_pnl(
    baseline_interchange_rate: float,
    committed_volume_m: float,
    avg_transaction_usd: float,
    discount_rate: float,
    deal_term_years: int,
    volume_growth_rate: float,
    npv_discount_rate: float = 0.08,
) -> pd.DataFrame:
    """
    Compute year-by-year P&L for a merchant acceptance deal.

    Args:
        baseline_interchange_rate: Standard interchange rate (e.g., 0.0195 = 1.95%)
        committed_volume_m: Committed annual transaction volume in millions
        avg_transaction_usd: Average transaction value in USD
        discount_rate: Discount off standard interchange (e.g., 0.10 = 10% off)
        deal_term_years: Length of deal in years (1-5)
        volume_growth_rate: Expected YoY volume growth (e.g., 0.05 = 5%)
        npv_discount_rate: Hurdle rate for NPV calculation (default 8%)

    Returns:
        DataFrame with columns: year, volume_m, gross_revenue, discount_cost,
        net_revenue, npv_contribution
    """
    rows = []
    for year in range(1, deal_term_years + 1):
        volume = committed_volume_m * 1_000_000 * (1 + volume_growth_rate) ** (year - 1)
        gross_revenue = volume * avg_transaction_usd * baseline_interchange_rate
        discount_cost = gross_revenue * discount_rate
        net_revenue = gross_revenue - discount_cost
        npv_contribution = net_revenue / (1 + npv_discount_rate) ** year
        rows.append({
            "year": year,
            "volume_m": volume / 1_000_000,
            "gross_revenue": gross_revenue,
            "discount_cost": discount_cost,
            "net_revenue": net_revenue,
            "npv_contribution": npv_contribution,
        })
    return pd.DataFrame(rows)
