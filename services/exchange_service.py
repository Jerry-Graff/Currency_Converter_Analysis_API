import requests
import os
from datetime import datetime, timedelta
from fastapi import HTTPException

BASE_URL = os.getenv("BASE_URL")


def fetch_90d_usd_gbp():
    """
    Fetch USD->GBP timeseries for the past 90 days (including today).
    Returns the parsed JSON dict from the API, something like:
    {
      'base': 'USD',
      'start_date': 'YYYY-MM-DD',
      'end_date': 'YYYY-MM-DD',
      'rates': {
        'YYYY-MM-DD': {'GBP': <rate>},
        ...
      }
    }
    """
    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=90)

    url = f"{BASE_URL}/timeseries"
    params = {
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "base": "USD",
        "symbols": "GBP"
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise HTTPException(
            status_code=500, detail="Error fetching 90-day timeseries data.")

    data = response.json()
    return data


def fetch_latest_usd_gbp():
    """
    Fetch the latest (today's) USD->GBP rate.
    Returns a float or raises an exception if not available.
    """
    url = f"{BASE_URL}/latest"
    params = {
        "base": "USD",
        "symbols": "GBP"
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise HTTPException(
            status_code=500, detail="Error fetching latest rate.")

    data = response.json()
    gbp_rate = data.get("rates", {}).get("GBP")
    if gbp_rate is None:
        raise HTTPException(
            status_code=404, detail="GBP rate not found in response.")
    return gbp_rate
