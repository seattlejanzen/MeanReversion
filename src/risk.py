import math
from src.config import MAX_RISK_PCT, STOP_BUFFER


def implied_stop(lower_band: float) -> float:
    """Stop price placed 1% below the lower Bollinger Band."""
    return lower_band * (1 - STOP_BUFFER)


def position_size(portfolio_value: float, entry_price: float, stop: float) -> int:
    """
    Size based on 2% portfolio risk rule:
        shares = (portfolio * MAX_RISK_PCT) / (entry - stop)

    Falls back to 1 share if the math produces zero.
    """
    risk_per_share = entry_price - stop
    if risk_per_share <= 0:
        return 1
    dollar_risk = portfolio_value * MAX_RISK_PCT
    qty = math.floor(dollar_risk / risk_per_share)
    return max(qty, 1)
