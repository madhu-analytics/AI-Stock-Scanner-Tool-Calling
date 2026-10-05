# AI Stock Scanner — Tool Calling

An AI-powered stock scanning project built with Python, OpenAI Tool Calling, and the BharatStock API.

## 📌 Project Overview

This project demonstrates how an LLM can understand a user's request and decide which Python tool/function should be called to retrieve and process stock market data.

The main goal is to build a foundation for an AI-powered stock scanner that can:

- Fetch current stock prices
- Fetch historical stock data
- Calculate technical indicators
- Scan multiple stocks
- Apply predefined screening rules
- Rank stocks based on clearly defined metrics
- Eventually expose these tools through MCP

> ⚠️ This project is for learning and technical experimentation. It does not provide personalized financial advice or guarantee future investment returns.

---

## 🧠 What is Tool Calling?

Tool calling allows an LLM to decide when it needs an external function to answer a user's request.

For example, if the user asks:

"Give me the current price of Reliance."

The LLM does not directly know the live market price.

Instead, it can decide to call a Python function such as:

`get_stock_price("RELIANCE")`

The Python function communicates with the BharatStock API and returns the actual market data.

The overall flow is:

User → main.py → LLM → Tool Call → Python Function → BharatStock API → Market Data → LLM → Final Response

---

## 🏗️ Project Architecture

The high-level architecture is:

User
↓
main.py
↓
OpenAI LLM
↓
Tool Selection
↓
Python Tool / Function
↓
BharatStock API
↓
Market Data
↓
Python Processing
↓
LLM
↓
Final Response

The LLM is responsible for understanding the user's request and deciding which tool is required.

Python is responsible for executing the actual functions and processing the data.

---

## 🛠️ Tools / Functions

The project uses Python functions as tools that can be called by the LLM.

### 1. get_stock_price()

Used to retrieve the current price of a stock.

Example:

`get_stock_price("RELIANCE")`

The function communicates with the BharatStock API and returns the available price information.

### 2. get_historical_stock_data()

Used to retrieve historical market data for a stock.

Historical data can be used for:

- Price analysis
- Returns
- Technical indicators
- Pattern detection
- Strategy evaluation
- Backtesting

Example:

`get_historical_stock_data("RELIANCE")`

### 3. calculate_rsi()

Calculates the Relative Strength Index (RSI) using historical price data.

RSI can be used as one of the technical indicators in the stock scanner.

### 4. calculate_all_rsi()

Calculates RSI values across the required historical data/timeframes.

The calculation is performed by Python rather than by the LLM.

### 5. scan_stocks()

This is the higher-level stock scanning function.

Instead of processing only one stock, the scanner can process a group of stocks and apply predefined screening logic.

The conceptual flow is:

Stock Universe → Historical Data → Indicators → Screening Rules → Matching Stocks → Ranking → Results

---

## 🤖 Why Use Python Functions Instead of Asking the LLM to Calculate Everything?

The LLM is responsible for:

- Understanding the user's request
- Deciding which tool to use
- Providing the required arguments
- Explaining the result

Python is responsible for:

- Calling APIs
- Fetching market data
- Calculating indicators
- Applying deterministic rules
- Processing large datasets
- Ranking/filtering data according to predefined logic

This separation makes the application more reliable, predictable, and easier to maintain.

---

## 🔄 Example Tool-Calling Flow

Suppose the user asks:

"What is the current price of TCS?"

The application sends the request to the LLM.

The LLM determines that it needs the stock-price tool.

It generates a tool call similar to:

`get_stock_price("TCS")`

Python executes the function.

The function calls BharatStock.

BharatStock returns the market data.

Python sends the result back to the LLM.

The LLM then generates the final response for the user.

This demonstrates the key concept of Tool Calling:

User → LLM → Tool → External API → Result → LLM → User

---

## 📊 Stock Scanner Goal

The long-term goal of this project is to create a scanner where a user can ask questions such as:

"Scan the stocks using my strategy."

or:

"Show me the top 5 stocks matching my criteria."

However, "top 5" must be based on a clearly defined metric.

Possible ranking metrics include:

- Highest return
- Highest volume
- RSI-based ranking
- Highest strategy score
- Highest RGB score
- Best historical performance according to a defined strategy

The ranking logic should be deterministic rather than allowing the LLM to invent its own ranking.

---

## 🎯 RGB Strategy

The project is intended to support an RGB-based stock screening strategy.

The exact RGB rules need to be explicitly defined before implementation.

The strategy may eventually evaluate factors such as:

- Candle direction
- Price movement
- Volume
- Historical behaviour
- Timeframe
- Other user-defined conditions

The scanner should apply the exact rules provided by the strategy rather than allowing the LLM to interpret or modify the strategy.

---

## ⏱️ Timeframes

The scanner can eventually support different timeframes such as:

- Daily
- Weekly
- Monthly
- Other supported intervals

The selected timeframe should be passed as a parameter to the appropriate data/tool function.

---

## 🧩 Project Structure

The project currently follows a structure similar to:

Day2/
├── main.py
├── market_data.py
├── scanner.py
├── indicators.py
├── req.txt
├── .env
└── myenv/

### main.py

Acts as the main application/orchestrator.

Responsibilities include:

- Loading environment variables
- Creating the OpenAI client
- Defining/using tools
- Sending user requests to the LLM
- Handling tool calls
- Returning the final response

### market_data.py

Responsible for communicating with the BharatStock API.

Keeping API communication separate from the main application makes the project easier to maintain.

### indicators.py

Contains technical-indicator calculations.

For example:

- RSI
- Other indicators added later

### scanner.py

Contains the stock-scanning logic.

This layer can:

- Process stocks
- Fetch historical data
- Apply indicators
- Apply strategy rules
- Filter results
- Rank matching stocks

---

## 🔐 Environment Variables

API keys and credentials should be stored in a `.env` file.

Example:

BHARATSTOCK_API_KEY=your_api_key
OPENAI_API_KEY=your_openai_api_key

Never upload `.env` to GitHub.

---

## 🚫 .gitignore

The project should contain a `.gitignore` file containing entries such as:

.env
myenv/
__pycache__/
*.pyc
.idea/
.DS_Store

This prevents secrets, virtual environments, Python cache files, IDE files, and other unnecessary files from being committed to GitHub.

---

## ⚠️ API Rate Limits

The BharatStock API has request limits depending on the plan.

A scanner that processes a large number of stocks can generate many API requests.

For example:

500 stocks × 1 historical-data request = 500 API requests

Therefore, a large stock universe should not simply be scanned with one API request per stock without considering:

- API limits
- Caching
- Batching
- Request optimisation
- Reusing historical data
- Incremental updates

This is an important engineering consideration when building a data-intensive AI application.

---

## 🧠 Important Design Principle

The LLM should not be responsible for the actual financial calculations.

Instead, the architecture should be:

LLM
↓
Understands request
↓
Chooses tool
↓
Python
↓
Gets data
↓
Calculates indicators
↓
Applies predefined rules
↓
Returns structured result
↓
LLM explains result

This creates a clear separation between AI reasoning/orchestration and deterministic data processing.

---

## 🆚 Day 1 vs Day 2

### Day 1 — Text-to-SQL

The Day 1 project demonstrated:

Natural Language → LLM → SQL → SQL Server → Data

The main challenge was teaching the LLM about the database schema and allowing it to generate SQL.

### Day 2 — Tool Calling

The Day 2 project demonstrates:

Natural Language → LLM → Tool Selection → Python Function → External API → Market Data → LLM Response

The important new concept is that the LLM can decide when to call a predefined Python function.

---

## 🚀 Future Improvements

Possible future improvements include:

- Support NIFTY 100
- Support NIFTY 500
- Build a stock-universe tool
- Add more technical indicators
- Implement the complete RGB strategy
- Add multiple timeframes
- Add caching
- Reduce API requests
- Add backtesting
- Add performance metrics
- Return structured scanner results
- Add a Streamlit UI
- Add MCP server support
- Expose stock tools through MCP
- Connect the MCP server to compatible AI clients

---

## 🔮 Future MCP Architecture

The next stage of the project can expose the stock functions through an MCP server.

The architecture would become:

ChatGPT / Claude / AI Client
↓
MCP
↓
MCP Server
↓
Python Tools
↓
BharatStock API

MCP does not replace the Python functions.

Instead, MCP provides a standard way for compatible AI applications to discover and use those tools.

The API credentials can remain inside the MCP server rather than being exposed to the AI client.

---

## 📚 Technologies Used

- Python
- OpenAI API
- OpenAI Tool Calling
- BharatStock API
- Pandas
- Technical Indicators
- Git
- GitHub
- PyCharm
- MCP — planned next step

---

## 🔒 Security

Never commit:

- API keys
- Passwords
- `.env`
- Private credentials

Always keep secrets in environment variables.

Before pushing the project to GitHub, verify that `.env` is ignored by Git.

---

## 🎓 What I Learned

Through this project I learned:

1. What AI Tool Calling is
2. How an LLM decides which tool to call
3. How Python functions can act as tools
4. How tools can communicate with external APIs
5. How to separate AI reasoning from deterministic calculations
6. How historical market data can be processed using Python
7. How technical indicators can be integrated into a scanner
8. Why API rate limits matter when building data-intensive applications
9. How an AI application can evolve toward MCP
10. How MCP can make tools reusable across different AI clients

---

## 📌 Project Status

Day 2 — AI Tool Calling / Stock Scanner

Current focus:

LLM
↓
Tool Calling
↓
Python Functions
↓
BharatStock API
↓
Market Data
↓
Indicators
↓
Stock Scanner

Future focus:

Stock Scanner
↓
Strategy Engine
↓
Backtesting
↓
MCP Server
↓
AI Client Integration

---

## ⚠️ Disclaimer

This project is built for educational and technical experimentation.

The scanner should use clearly defined, deterministic rules and historical data for analysis. Historical performance does not guarantee future results, and the output should not be treated as personalized investment advice.

---

## 👩‍💻 Learning Journey

This project is part of my hands-on journey into:

- AI
- LLMs
- Tool Calling
- Generative AI
- Python
- Data Engineering
- API Integration
- Technical Data Processing
- MCP
- AI-powered applications

Day 1: Text-to-SQL with SQL Server

Day 2: AI Tool Calling and Stock Scanner

Next: Strategy Engine → Backtesting → MCP
