from fastapi import FastAPI, HTTPException
from datetime import datetime, timedelta
from typing import Dict, Any
import requests
import os

app = FastAPI(
    title="USD to GBP Concersion Helper",
    description="Use historical exhcnage rates to help decide whent to convert your $",
    version="1.0.0"
)

BASE_URL = os.getenv("BASE_URL")


def fetch_timeseries_rates(start_date: str, end_date: str, base: str = "USD", symbols: str = "GBP") -> Dict[str, Any]:

    url = f"{BASE_URL}/timeseries"
    params = {
        "start_date": start_date,
        "end_date": end_date,
        "base": base,
        "symbols": symbols
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error fetching timeseries data")
    return response.json()


def fetch_latest_rate(base: str = "USD", symbols: str = "GBP") -> float:

    url = f"{BASE_URL}/latest"
    params = {
        "base": base,
        "symbols": symbols
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error fetchign latest rates")
    data = response.json()
    return data["rates"].get(symbols, None)