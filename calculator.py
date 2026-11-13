def calculate_levels(nifty_close, india_vix):
    if nifty_close <= 0 or india_vix <= 0:
        raise ValueError("Nifty close and India VIX must be positive")

    volatility_1 = (india_vix / 19.1) / 100
    volatility_2 = (19.1 / india_vix) / 100

    return {
        "high_1": round(nifty_close * (1 + volatility_1)),
        "high_2": round(nifty_close * (1 + volatility_2)),
        "low_1": round(nifty_close * (1 - volatility_1)),
        "low_2": round(nifty_close * (1 - volatility_2)),
    }
