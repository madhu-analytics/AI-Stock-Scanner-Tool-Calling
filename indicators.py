# indicators.py

import pandas as pd


def calculate_rsi(close_prices, period=14):
    """
    Calculate RSI using Wilder's smoothing method.
    """

    prices = pd.Series(close_prices, dtype="float64")

    delta = prices.diff()

    gains = delta.clip(lower=0)
    losses = -delta.clip(upper=0)

    average_gain = gains.ewm(
        alpha=1 / period,
        min_periods=period,
        adjust=False
    ).mean()

    average_loss = losses.ewm(
        alpha=1 / period,
        min_periods=period,
        adjust=False
    ).mean()

    rs = average_gain / average_loss

    rsi = 100 - (100 / (1 + rs))

    return rsi


def calculate_daily_rsi(df, period=14):
    """
    Calculate RSI using daily closing prices.
    """

    data = df.copy()

    data["date"] = pd.to_datetime(data["date"])
    data = data.sort_values("date")

    return calculate_rsi(data["close"], period)


def calculate_weekly_rsi(df, period=14):
    """
    Convert daily closing prices into weekly closing prices
    and calculate RSI.
    """

    data = df.copy()

    data["date"] = pd.to_datetime(data["date"])
    data = data.sort_values("date")
    data = data.set_index("date")

    weekly_close = data["close"].resample("W-FRI").last()

    # Remove the current incomplete week
    latest_date = data.index.max()
    current_week_friday = latest_date + pd.offsets.Week(
        weekday=4
    )

    weekly_close = weekly_close[
        weekly_close.index < current_week_friday
    ]

    return calculate_rsi(weekly_close, period)


def calculate_monthly_rsi(df, period=14):
    """
    Convert daily closing prices into completed monthly
    closing prices and calculate RSI.
    """

    data = df.copy()

    data["date"] = pd.to_datetime(data["date"])
    data = data.sort_values("date")
    data = data.set_index("date")

    monthly_close = data["close"].resample("ME").last()

    # Remove current incomplete month
    latest_date = data.index.max()
    current_month = latest_date.to_period("M")

    monthly_close = monthly_close[
        monthly_close.index.to_period("M") < current_month
    ]

    return calculate_rsi(monthly_close, period)
def calculate_all_rsi(df, period=14):
    """
    Calculate the latest RSI for Daily, Weekly and Monthly
    timeframes.

    Returns:
        Dictionary containing the latest RSI values.
    """

    daily_rsi = calculate_daily_rsi(df, period)
    weekly_rsi = calculate_weekly_rsi(df, period)
    monthly_rsi = calculate_monthly_rsi(df, period)

    return {
        "daily_rsi": daily_rsi.iloc[-1],
        "weekly_rsi": weekly_rsi.iloc[-1],
        "monthly_rsi": monthly_rsi.iloc[-1]
    }