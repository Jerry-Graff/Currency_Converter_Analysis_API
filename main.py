import os
import requests
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Currency Converter API",
    description="Convert USD to other currencies using ExchangeRateAPI",
    version="1.0.0"
)

API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")
BASE_URL = os.getenv("BASE_URL")


class ConversionResponse(BaseModel):
    base: str
    target: str
    ammount: float
    converted_ammount: float


@app.get("/convert", response_model=ConversionResponse)
def convert_currency(target: str = "GBP", ammount: float = 1.0):
    """
    Convert USD to a target currency.
    - target: Currency code (e.g., GBP, EUR, JPY)
    - amount: USD amount to convert
    """
    try:
        # Fetch exchange rates
        response = requests.get(f"{BASE_URL}/{API_KEY}/latest/USD")
        response.raise_for_status()  # Raise error for bad status codes
        data = response.json()

        # Check target currency exsists
        if target not in data["conversion_rates"]:
            raise HTTPException(
                status_code=400, detail="Invalid target currency")

        rate = data["conversion_rates"][target]
        converted_ammount = ammount * rate

        return {
            "base": "USD",
            "target": target,
            "ammount": ammount,
            "converted_ammount": round(converted_ammount, 2)
        }

    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500, detail=f"API request failed: {str(e)}")
    except KeyError:
        raise HTTPException(
            status_code=500, detail="Invalid API response format")
