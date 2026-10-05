import os
from dotenv import load_dotenv
from bharatstock import BharatStock
import inspect

load_dotenv()
api_key = os.getenv("BHARATSTOCK_API_KEY")
client = BharatStock(api_key=api_key)


print("BharatStock client connected!")

def get_stock_price(symbol):
    stock = client.stocks.get(symbol)

    return {
        "symbol": stock.symbol,
        "company_name": stock.company_name,
        "price": stock.latest_price.close,
        "trade_date": stock.latest_price.trade_date
    }

#result = get_stock_price("TCS")
#print(result)

def get_historical_stock_data(symbol, from_date, to_date):

    first_page = client.stocks.prices(
        symbol,
        from_date=from_date,
        to_date=to_date,
        page=1,
        page_size=100
    )

    all_data = first_page.data

    for page in range(2, first_page.total_pages + 1):

        next_page = client.stocks.prices(
            symbol,
            from_date=from_date,
            to_date=to_date,
            page=page,
            page_size=100
        )

        all_data.extend(next_page.data)

    return [
        {
            "symbol": symbol,
            "date": str(point.trade_date),
            "open": point.open,
            "high": point.high,
            "low": point.low,
            "close": point.close,
            "volume": point.volume
        }
        for point in all_data
    ]
#result = get_historical_stock_data(
   # "TCS",
  #  "2026-09-02",
 #   "2026-09-02"
#)

#print(result)