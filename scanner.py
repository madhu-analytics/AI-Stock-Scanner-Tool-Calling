
from market_data import get_historical_stock_data
from indicators import calculate_all_rsi
import pandas as pd


def scan_stock(symbol):

    historical_data = get_historical_stock_data(
        symbol,
        "2025-09-23",
        "2026-09-18"
    )

    df = pd.DataFrame(historical_data)

    rsi_values = calculate_all_rsi(df)

    daily_rsi = rsi_values["daily_rsi"]
    weekly_rsi = rsi_values["weekly_rsi"]
    monthly_rsi = rsi_values["monthly_rsi"]

    if pd.isna(monthly_rsi):
        return {
            "symbol": symbol,
            "daily_rsi": float(daily_rsi),
            "weekly_rsi": float(weekly_rsi),
            "monthly_rsi": None,
            "passes": False,
            "status": "INSUFFICIENT_HISTORY"
        }

    passes = (
            daily_rsi > 60
            and weekly_rsi > 60
            and monthly_rsi > 60
    )

    return {
        "symbol": symbol,
        "daily_rsi": float(daily_rsi),
        "weekly_rsi": float(weekly_rsi),
        "monthly_rsi": float(monthly_rsi),
        "passes": passes,
        "status": "PASS" if passes else "FAIL"
    }


def scan_stocks(symbols):

    results = []

    for symbol in symbols:

        result = scan_stock(symbol)

        results.append(result)

    return results





