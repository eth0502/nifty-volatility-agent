
def test_python_is_working():
    assert 1 + 1 == 2


def test_agent_basic_values():
    nifty = 24000
    vix = 15

    assert nifty > 0
    assert vix >= 0


def test_percentage_calculation():
    previous_vix = 15
    current_vix = 16

    change = ((current_vix - previous_vix) / previous_vix) * 100

    assert round(change, 2) == 6.67
