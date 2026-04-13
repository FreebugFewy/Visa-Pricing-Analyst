import pytest
from utils.opportunity_score import compute_opportunity_score


def test_zero_volume_returns_zero():
    score = compute_opportunity_score(
        annual_volume_m=0.0,
        avg_transaction_usd=100.0,
        interchange_rate=0.024,
        acceptance_rate=0.90,
        yoy_growth_rate=0.10,
    )
    assert score == pytest.approx(0.0)


def test_perfect_acceptance_sets_network_gap_to_one():
    # network_gap_multiplier = 2.0 - 1.0 = 1.0
    # score = gross_revenue * growth_multiplier * network_gap_multiplier
    #       = (annual_volume_m * avg_transaction_usd * interchange_rate) * 1.0 * 1.0
    score = compute_opportunity_score(
        annual_volume_m=10.0,
        avg_transaction_usd=100.0,
        interchange_rate=0.020,
        acceptance_rate=1.0,
        yoy_growth_rate=0.0,
    )
    assert score == pytest.approx(10.0 * 100.0 * 0.020 * 1.0 * 1.0)


def test_zero_growth_applies_no_growth_multiplier():
    # growth_multiplier = 1 + 0 = 1.0, so score = gross_revenue * network_gap
    score = compute_opportunity_score(
        annual_volume_m=10.0,
        avg_transaction_usd=100.0,
        interchange_rate=0.020,
        acceptance_rate=0.90,
        yoy_growth_rate=0.0,
    )
    expected = 10.0 * 100.0 * 0.020 * 1.0 * (2.0 - 0.90)
    assert score == pytest.approx(expected)


def test_higher_volume_produces_higher_score():
    base_kwargs = dict(avg_transaction_usd=100.0, interchange_rate=0.024,
                       acceptance_rate=0.90, yoy_growth_rate=0.10)
    low = compute_opportunity_score(annual_volume_m=50.0, **base_kwargs)
    high = compute_opportunity_score(annual_volume_m=100.0, **base_kwargs)
    assert high > low


def test_higher_growth_produces_higher_score():
    base_kwargs = dict(annual_volume_m=50.0, avg_transaction_usd=100.0,
                       interchange_rate=0.024, acceptance_rate=0.90)
    low = compute_opportunity_score(yoy_growth_rate=0.05, **base_kwargs)
    high = compute_opportunity_score(yoy_growth_rate=0.20, **base_kwargs)
    assert high > low


def test_lower_acceptance_rate_produces_higher_score():
    # Lower acceptance = more room to improve = higher network gap multiplier
    base_kwargs = dict(annual_volume_m=50.0, avg_transaction_usd=100.0,
                       interchange_rate=0.024, yoy_growth_rate=0.10)
    low_gap = compute_opportunity_score(acceptance_rate=0.95, **base_kwargs)
    high_gap = compute_opportunity_score(acceptance_rate=0.82, **base_kwargs)
    assert high_gap > low_gap


def test_zero_interchange_rate_returns_zero():
    score = compute_opportunity_score(
        annual_volume_m=50.0,
        avg_transaction_usd=100.0,
        interchange_rate=0.0,
        acceptance_rate=0.90,
        yoy_growth_rate=0.10,
    )
    assert score == pytest.approx(0.0)
