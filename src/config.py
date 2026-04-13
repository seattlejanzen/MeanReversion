import os
from dotenv import load_dotenv

load_dotenv()

ALPACA_API_KEY = os.environ["ALPACA_API_KEY"]
ALPACA_SECRET_KEY = os.environ["ALPACA_SECRET_KEY"]
ALPACA_BASE_URL = os.environ.get("ALPACA_BASE_URL", "https://paper-api.alpaca.markets")

# Universe
SYMBOLS = ["AAPL", "MSFT", "NVDA", "AMD", "META", "GOOGL", "AMZN"]

# RSI
RSI_PERIOD = 14
RSI_ENTRY = 30     # buy when RSI drops below this
RSI_EXIT = 50      # close when RSI recovers above this

# Bollinger Bands
BB_PERIOD = 20
BB_STD = 2.0

# Risk management
MAX_RISK_PCT = 0.02   # risk at most 2% of portfolio per trade
STOP_BUFFER = 0.01    # implied stop placed 1% below the lower band
