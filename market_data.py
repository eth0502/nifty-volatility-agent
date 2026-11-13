
import requests
import json
from datetime import datetime
from zoneinfo import ZoneInfo

NSE_URL = "https://www.nseindia.com/api/allIndices"
NSE_HOME = "https://www.nseindia.com"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Referer": NSE_HOME,
}


def fetch_market_data():
    session = requests.Session()
    session.headers.update(HEADERS)

    home = session.get(NSE_HOME, timeout=20)
    home.raise_for_status()

    response = session.get(NSE_URL, timeout=20)
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
        raise ValueError("Nifty 50 or India VIX missing from NSE response")

    # Print complete VIX record for field/timestamp verification
    print("NSE INDIA VIX RAW DATA:")
    print(json.dumps(vix, indent=2))

    nifty_close = float(nifty["previousClose"])
    india_vix = float(vix["last"])

    if nifty_close <= 0 or india_vix <= 0:
        raise ValueError("Invalid market values")

    # Do not confuse fetch time with exchange quote time.
    quote_timestamp = (
        vix.get("time")
        or vix.get("lastUpdateTime")
        or vix.get("timestamp")
    )

    return {
        "nifty_previous_close": nifty_close,
        "india_vix": india_vix,
        "vix_quote_timestamp": quote_timestamp,
        "source": "NSE India",
        "fetched_at": datetime.now(
            ZoneInfo("Asia/Kolkata")
        ).isoformat(),
        "warning": (
            "VIX quote freshness is NOT verified. "
            "Do not treat fetched_at as exchange quote time."
        )
    }


if __name__ == "__main__":
    print(json.dumps(fetch_market_data(), indent=2))
