from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta
import pandas as pd

from src.config import ALPACA_API_KEY, ALPACA_SECRET_KEY


class AlpacaBroker:
    def __init__(self):
        self.trading = TradingClient(ALPACA_API_KEY, ALPACA_SECRET_KEY, paper=True)
        self.data = StockHistoricalDataClient(ALPACA_API_KEY, ALPACA_SECRET_KEY)

    def get_account(self):
        return self.trading.get_account()

    def get_portfolio_value(self) -> float:
        return float(self.trading.get_account().portfolio_value)

    def get_positions(self) -> dict:
        positions = self.trading.get_all_positions()
        return {p.symbol: p for p in positions}

    def get_bars(self, symbol: str, lookback_days: int = 90) -> pd.DataFrame:
        start = datetime.utcnow() - timedelta(days=lookback_days)
        request = StockBarsRequest(
            symbol_or_symbols=symbol,
            timeframe=TimeFrame.Day,
            start=start,
        )
        bars = self.data.get_stock_bars(request)
        df = bars.df
        if isinstance(df.index, pd.MultiIndex):
            df = df.xs(symbol, level="symbol")
        return df

    def submit_order(self, symbol: str, qty: float, side: str) -> object:
        order_side = OrderSide.BUY if side == "buy" else OrderSide.SELL
        request = MarketOrderRequest(
            symbol=symbol,
            qty=qty,
            side=order_side,
            time_in_force=TimeInForce.DAY,
        )
        return self.trading.submit_order(request)

    def close_position(self, symbol: str) -> object:
        return self.trading.close_position(symbol)
