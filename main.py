from openai import OpenAI
from dotenv import load_dotenv
from market_data import get_stock_price, get_historical_stock_data
from scanner import scan_stocks
import json


load_dotenv()

client = OpenAI()


my_tools = [

    # --------------------------------------------------
    # TOOL 1: Get latest stock price
    # --------------------------------------------------

    {
        "type": "function",
        "name": "get_stock_price",
        "description": "Get the latest available stock price for an Indian stock.",
        "parameters": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "The stock symbol, for example RELIANCE or TCS."
                }
            },
            "required": ["symbol"],
            "additionalProperties": False
        }
    },

    # --------------------------------------------------
    # TOOL 2: Get historical stock data
    # --------------------------------------------------

    {
        "type": "function",
        "name": "get_historical_stock_data",
        "description": "Get historical daily stock price data for an Indian stock between two dates.",
        "parameters": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "The stock symbol, for example TCS or RELIANCE."
                },
                "from_date": {
                    "type": "string",
                    "description": "Start date in YYYY-MM-DD format."
                },
                "to_date": {
                    "type": "string",
                    "description": "End date in YYYY-MM-DD format."
                }
            },
            "required": [
                "symbol",
                "from_date",
                "to_date"
            ],
            "additionalProperties": False
        }
    },

    # --------------------------------------------------
    # TOOL 3: Scan multiple stocks
    # --------------------------------------------------

    {
        "type": "function",
        "name": "scan_stocks",
        "description": "Scan multiple Indian stocks using Daily, Weekly and Monthly RSI screening criteria.",
        "parameters": {
            "type": "object",
            "properties": {
                "symbols": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "List of Indian stock symbols to scan, for example ['TCS', 'RELIANCE']."
                }
            },
            "required": [
                "symbols"
            ],
            "additionalProperties": False
        }
    }
]


# --------------------------------------------------
# 1. Ask the user
# --------------------------------------------------

question = input("Enter your question: ")


# --------------------------------------------------
# 2. Ask OpenAI
# --------------------------------------------------

response = client.responses.create(
    model="gpt-5.6-sol",
    input=question,
    tools=my_tools,
    tool_choice="required"
)


# --------------------------------------------------
# 3. Look for tool calls
# --------------------------------------------------

tool_results = []

for item in response.output:

    if item.type == "function_call":

        arguments = json.loads(item.arguments)

        # ------------------------------------------
        # Tool 1
        # ------------------------------------------

        if item.name == "get_stock_price":

            result = get_stock_price(
                arguments["symbol"]
            )

        # ------------------------------------------
        # Tool 2
        # ------------------------------------------

        elif item.name == "get_historical_stock_data":

            result = get_historical_stock_data(
                arguments["symbol"],
                arguments["from_date"],
                arguments["to_date"]
            )

        # ------------------------------------------
        # Tool 3
        # ------------------------------------------

        elif item.name == "scan_stocks":

            result = scan_stocks(
                arguments["symbols"]
            )

        # ------------------------------------------
        # Send tool result
        # ------------------------------------------

        tool_results.append({
            "type": "function_call_output",
            "call_id": item.call_id,
            "output": json.dumps(
                result,
                default=str
            )
        })


# --------------------------------------------------
# 4. Send tool result back to OpenAI
# --------------------------------------------------

final_response = client.responses.create(
    model="gpt-5.6-sol",
    previous_response_id=response.id,
    input=tool_results
)


# --------------------------------------------------
# 5. Print final answer
# --------------------------------------------------

print("\nFinal answer:")
print(final_response.output_text)