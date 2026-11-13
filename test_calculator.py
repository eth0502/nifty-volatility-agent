import pytest
from calculator import calculate_levels


def test_calculation():
    result = calculate_levels(24000, 20)

    assert result == {
        "high_1": 24251,
        "high_2": 24229,
        "low_1": 23749,
        "low_2": 23771,
    }


def test_invalid_nifty():
    with pytest.raises(ValueError):
        calculate_levels(0, 20)


def test_invalid_vix():
    with pytest.raises(ValueError):
        calculate_levels(24000, 0)
