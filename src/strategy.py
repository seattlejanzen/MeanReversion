from dataclasses import dataclass
import pandas as pd
import numpy as np

from src.config import RSI_PERIOD, RSI_ENTRY, RSI_EXIT, BB_PERIOD, BB_STD

MIN_BARS = BB_PERIOD + RSI_PERIOD + 5  # minimum bars needed for reliable signals


@dataclass
class Indicators:
    rsi: float
    price: float
    bb_upper: float
    bb_middle: float  # 20-period SMA — the mean-reversion target
    bb_lower: float


def _compute_rsi(prices: pd.Series, period: int) -> pd.Series:
    delta = prices.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(com=period - 1, min_periods=period).mean()
    avg_loss = loss.ewm(com=period - 1, min_periods=period).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def compute_indicators(prices: pd.Series) -> Indicators | None:
    """Return latest indicator values, or None if insufficient data."""
    if len(prices) < MIN_BARS:
        return None

    rsi_series = _compute_rsi(prices, RSI_PERIOD)
    sma = prices.rolling(BB_PERIOD).mean()
    std = prices.rolling(BB_PERIOD).std()

    bb_middle = float(sma.iloc[-1])
    bb_upper = float((sma + BB_STD * std).iloc[-1])
    bb_lower = float((sma - BB_STD * std).iloc[-1])
    rsi = float(rsi_series.iloc[-1])
    price = float(prices.iloc[-1])

    return Indicators(
        rsi=rsi,
        price=price,
        bb_upper=bb_upper,
        bb_middle=bb_middle,
        bb_lower=bb_lower,
    )


def get_signal(ind: Indicators, in_position: bool) -> str:
    """
    Returns one of: 'buy', 'close', 'hold'.

    Entry  — RSI < RSI_ENTRY (30) AND price <= lower Bollinger Band
    Exit   — RSI > RSI_EXIT (50) OR price >= middle band (20-SMA)
    """
    if in_position:
        if ind.rsi > RSI_EXIT or ind.price >= ind.bb_middle:
            return "close"
        return "hold"

    if ind.rsi < RSI_ENTRY and ind.price <= ind.bb_lower:
        return "buy"

    return "hold"
