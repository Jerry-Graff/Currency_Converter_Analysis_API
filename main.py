from fastapi import FastAPI, HTTPException
from services.exchange_service import fetch_90d_usd_gbp, fetch_latest_usd_gbp
from services.analysis_service import extract_usd_gbp_rates, analyze_90d, is_good_day

app = FastAPI(
    title="USD to GBP Currency App",
    description="Fetch the past 90 days of USD->GBP",
    version="1.0.0"
)


@app.get("/analysis", summary="Analyze 90-day historical USD->GBP.")
def get_analysis(threshold: float = 0.0):
    """
    1. Fetch 90 days of historical USD->GBP rates.
    2. Fetch the current (today) USD->GBP rate.
    3. Analyze them to see if it's a good day to convert.
    4. Return relevant data points.

    :param threshold: The threshold above the average for deciding "good day".
    """
    try:
        # 1. Fetch historical timeseries data (90 days).
        timeseries_data = fetch_90d_usd_gbp()
        historical_rates = extract_usd_gbp_rates(timeseries_data)

        # 2. Fetch today's rate.
        current = fetch_latest_usd_gbp()

        # 3. Analyze.
        stats = analyze_90d(current, historical_rates)
        recommendation = is_good_day(
            current_rate=stats["current_rate"],
            avg_rate=stats["average_90d"],
            threshold=threshold
        )

        # 4. Return the response as JSON.
        return {
            "current_rate": stats["current_rate"],
            "average_rate_90d": stats["average_90d"],
            "min_rate_90d": stats["min_90d"],
            "max_rate_90d": stats["max_90d"],
            "difference_from_average": stats["difference_from_average"],
            "recommendation": "Yes" if recommendation else "No",
            "threshold_used": threshold
        }
    except HTTPException as e:
        # FastAPI will auto-handle HTTPException with correct status codes.
        raise e
    except Exception as e:
        # Catch other unexpected errors
        raise HTTPException(status_code=500, detail=str(e))
