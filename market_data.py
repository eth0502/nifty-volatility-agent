
import requests
import json
from datetime import datetime
from zoneinfo import ZoneInfo

NSE_URL = "https://www.nseindia.com/api/allIndices"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.nseindia.com/",
    "Accept-Language": "en-US,en;q=0.9",
}


def fetch_market_data():
    session = requests.Session()
    session.headers.update(HEADERS)

    try:
        response = session.get(NSE_URL, timeout=20)

        if response.status_code == 403:
            raise RuntimeError(
                "NSE blocked GitHub Actions server (HTTP 403). "
                "A different verified data source is required."
            )

        response.raise_for_status()
        data = response.json()

    except requests.RequestException as error:
        raise RuntimeError(f"NSE request failed: {error}") from error

    indices = data.get("data", [])

    nifty = next(
        (item for item in indices if item.get("index") == "NIFTY 50"),
        None
    )

    vix = next(
        (item for item in indices if item.get("index") == "INDIA VIX"),
        None
    )

    if nifty is None or vix is None:
        raise ValueError("Nifty 50 or India VIX missing in NSE response")

    print("RAW NIFTY DATA:")
    print(json.dumps(nifty, indent=2))

    print("RAW INDIA VIX DATA:")
    print(json.dumps(vix, indent=2))

    nifty_close = float(nifty["previousClose"])
    india_vix = float(vix["last"])

    if nifty_close <= 0 or india_vix <= 0:
        raise ValueError("Invalid market values")

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
        "verified_live": False
    }


if __name__ == "__main__":
    result = fetch_market_data()
    print(json.dumps(result, indent=2))
