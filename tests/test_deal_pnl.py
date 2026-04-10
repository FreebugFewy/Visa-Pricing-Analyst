import pytest
from utils.deal_pnl import compute_deal_pnl


def test_returns_one_row_per_year():
    df = compute_deal_pnl(
        baseline_interchange_rate=0.019,
        committed_volume_m=50.0,
        avg_transaction_usd=85.0,
        discount_rate=0.10,
        deal_term_years=3,
        volume_growth_rate=0.05,
    )
    assert len(df) == 3


def test_year_1_volume_equals_committed_volume():
    df = compute_deal_pnl(
        baseline_interchange_rate=0.019,
        committed_volume_m=50.0,
        avg_transaction_usd=85.0,
        discount_rate=0.10,
        deal_term_years=3,
        volume_growth_rate=0.05,
    )
    assert df.loc[0, "volume_m"] == pytest.approx(50.0)


def test_year_2_volume_reflects_growth_rate():
    # 50M * 1.10^1 = 55M
    df = compute_deal_pnl(
        baseline_interchange_rate=0.019,
        committed_volume_m=50.0,
        avg_transaction_usd=85.0,
        discount_rate=0.10,
        deal_term_years=3,
        volume_growth_rate=0.10,
    )
    assert df.loc[1, "volume_m"] == pytest.approx(55.0)


def test_gross_revenue_is_volume_times_avg_txn_times_rate():
    # 10M txns * $100 * 2.0% = $20,000,000
    df = compute_deal_pnl(
        baseline_interchange_rate=0.020,
        committed_volume_m=10.0,
        avg_transaction_usd=100.0,
        discount_rate=0.0,
        deal_term_years=1,
        volume_growth_rate=0.0,
    )
    assert df.loc[0, "gross_revenue"] == pytest.approx(20_000_000.0)


def test_zero_discount_means_gross_equals_net():
    df = compute_deal_pnl(
        baseline_interchange_rate=0.019,
        committed_volume_m=50.0,
        avg_transaction_usd=85.0,
        discount_rate=0.0,
        deal_term_years=3,
        volume_growth_rate=0.05,
    )
    for _, row in df.iterrows():
        assert row["gross_revenue"] == pytest.approx(row["net_revenue"])


def test_discount_cost_equals_gross_minus_net():
    df = compute_deal_pnl(
        baseline_interchange_rate=0.019,
        committed_volume_m=50.0,
        avg_transaction_usd=85.0,
        discount_rate=0.15,
        deal_term_years=3,
        volume_growth_rate=0.05,
    )
    for _, row in df.iterrows():
        assert row["discount_cost"] == pytest.approx(row["gross_revenue"] - row["net_revenue"])


def test_npv_contribution_uses_hurdle_rate():
    # 10M txns * $100 * 2% = $20M net (no discount). Year 1 NPV = 20M / 1.08
    df = compute_deal_pnl(
        baseline_interchange_rate=0.020,
        committed_volume_m=10.0,
        avg_transaction_usd=100.0,
        discount_rate=0.0,
        deal_term_years=2,
        volume_growth_rate=0.0,
        npv_discount_rate=0.08,
    )
    assert df.loc[0, "npv_contribution"] == pytest.approx(20_000_000.0 / 1.08)


def test_zero_growth_produces_identical_volume_each_year():
    df = compute_deal_pnl(
        baseline_interchange_rate=0.019,
        committed_volume_m=50.0,
        avg_transaction_usd=85.0,
        discount_rate=0.10,
        deal_term_years=4,
        volume_growth_rate=0.0,
    )
    assert df["volume_m"].nunique() == 1
