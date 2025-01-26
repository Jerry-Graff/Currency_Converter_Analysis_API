from typing import Dict, Any, List
from fastapi import HTTPException


def extract_usd_gbp_rates(timeseries_data: Dict[str, Any]) -> List[float]:
    """
    Takes the 90-day timeseries data (in the format from exchangerate.host)
    and extracts the daily GBP rates as a list of floats.
    """
    if "rates" not in timeseries_data:
        raise HTTPException(
            status_code=500, detail="Timeseries data invalid: missing 'rates'.")

    gbp_rates = []
    for date_str, rate_obj in timeseries_data["rates"].items():
        gbp_rate = rate_obj.get("GBP")
        if gbp_rate is not None:
            gbp_rates.append(gbp_rate)

    if not gbp_rates:
        raise HTTPException(
            status_code=500, detail="No GBP rates found in timeseries data.")

    return gbp_rates


def analyze_90d(current_rate: float, historical_rates: list[float]) -> Dict[str, float]:
    """
    Given today's rate and a list of historical rates (from the past 90 days),
    compute the average, min, max, and how far current is above/below the
    average.

    Returns a dict with the computed values.
    """
    avg_rate = sum(historical_rates) / len(historical_rates)
    min_rate = min(historical_rates)
    max_rate = max(historical_rates)
    difference_from_avg = current_rate - avg_rate  # positive if current is higher than avg

    return {
        "current_rate": current_rate,
        "average_90d": avg_rate,
        "min_90d": min_rate,
        "max_90d": max_rate,
        "difference_from_average": difference_from_avg
    }


def is_good_day(current_rate: float, avg_rate: float, threshold: float = 0.0) -> bool:
    """
    Simple heuristic: if current_rate is greater than (average + threshold), We
    say it's a good day to convert (since you're getting more GBP for your USD)

    You can adjust threshold as needed (e.g., 0.005).
    """
    return current_rate > (avg_rate + threshold)
