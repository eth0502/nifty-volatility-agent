
import requests
import json
from datetime import datetime
from zoneinfo import ZoneInfo

NSE_URL = "https://www.nseindia.com/api/allIndices"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.nseindia.com/",
}


def fetch_market_data():
    response = requests.get(
        NSE_URL,
        headers=HEADERS,
        timeout=20
    )
    response.raise_for_status()

    indices = response.json().get("data", [])

    nifty = next(
        (x for x in indices if x.get("index") == "NIFTY 50"),
        None
    )

    vix = next(
        (x for x in indices if x.get("index") == "INDIA VIX"),
        None
    )

    if not nifty or not vix:
        raise ValueError("Nifty 50 or India VIX missing")

    nifty_close = float(nifty["previousClose"])
    vix_live = float(vix["last"])
    vix_previous_day = float(vix["previousDayVal"])

    if min(nifty_close, vix_live, vix_previous_day) <= 0:
        raise ValueError("Invalid market data")

    return {
        "nifty_previous_close": nifty_close,
        "india_vix_latest": vix_live,
        "india_vix_previous_day_reference": vix_previous_day,
        "source": "NSE India",
        "fetched_at": datetime.now(
            ZoneInfo("Asia/Kolkata")
        ).isoformat()
    }


if __name__ == "__main__":
    print(json.dumps(fetch_market_data(), indent=2))
