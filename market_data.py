import requests
import json
import re
from datetime import datetime
from zoneinfo import ZoneInfo

NSE_URL = "https://www.nseindia.com/api/allIndices"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.nseindia.com/"
}


def fetch_market_data():
    session = requests.Session()
    session.headers.update(HEADERS)

    # Establish NSE session
    session.get(
        "https://www.nseindia.com",
        timeout=20
    )

    response = session.get(
        NSE_URL,
        timeout=20
    )
    response.raise_for_status()

    data = response.json()
    indices = data.get("data", [])

    nifty = next(
        (x for x in indices if x.get("index") == "NIFTY 50"),
        None
    )

    vix = next(
        (x for x in indices if x.get("index") == "INDIA VIX"),
        None
    )

    if not nifty or not vix:
        raise ValueError("Nifty 50 or India VIX missing from NSE data")

    nifty_close = float(nifty["previousClose"])
    india_vix = float(vix["last"])

    if nifty_close <= 0 or india_vix <= 0:
        raise ValueError("Invalid market values")

    return {
        "nifty_previous_close": nifty_close,
        "india_vix": india_vix,
        "source": "NSE India",
        "fetched_at": datetime.now(
            ZoneInfo("Asia/Kolkata")
        ).isoformat()
    }


if __name__ == "__main__":
    print(json.dumps(fetch_market_data(), indent=2))
  
