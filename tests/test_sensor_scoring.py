import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "backend"))

from app.api.sensors import calculate_spoilage_score


def test_optimal_cold_chain_conditions_have_no_risk_score():
    assert calculate_spoilage_score(5, 90, "berries") == 0


def test_extreme_temperature_is_higher_risk_than_optimal_conditions():
    assert calculate_spoilage_score(40, 90, "berries") > calculate_spoilage_score(5, 90, "berries")


def test_humidity_and_temperature_scores_are_bounded():
    score = calculate_spoilage_score(-50, 100, "berries")
    assert 0 <= score <= 1


def test_commodity_specific_storage_profiles_are_respected():
    dry_grain_score = calculate_spoilage_score(10, 50, "grains")
    wet_grain_score = calculate_spoilage_score(10, 90, "grains")
    assert dry_grain_score < wet_grain_score