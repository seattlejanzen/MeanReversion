import logging
from src.broker import AlpacaBroker
from src.strategy import compute_indicators, get_signal
from src.risk import implied_stop, position_size
from src.config import SYMBOLS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)


def run():
    broker = AlpacaBroker()
    portfolio_value = float(broker.get_account().portfolio_value)
    log.info(f"Portfolio value: ${portfolio_value:,.2f}")

    open_positions = broker.get_positions()

    for symbol in SYMBOLS:
        try:
            bars = broker.get_bars(symbol)
            ind = compute_indicators(bars["close"])

            if ind is None:
                log.warning(f"{symbol}: insufficient data, skipping")
                continue

            in_pos = symbol in open_positions
            signal = get_signal(ind, in_pos)

            log.info(
                f"{symbol}: price={ind.price:.2f}  RSI={ind.rsi:.1f}  "
                f"BB=[{ind.bb_lower:.2f}, {ind.bb_middle:.2f}, {ind.bb_upper:.2f}]  "
                f"in_pos={in_pos}  signal={signal}"
            )

            if signal == "close":
                broker.close_position(symbol)
                log.info(f"  [{symbol}] Closed long position")

            elif signal == "buy":
                stop = implied_stop(ind.bb_lower)
                qty = position_size(portfolio_value, ind.price, stop)
                dollar_risk = qty * (ind.price - stop)
                broker.submit_order(symbol, qty, "buy")
                log.info(
                    f"  [{symbol}] Bought {qty} shares @ ~${ind.price:.2f}  "
                    f"stop=${stop:.2f}  dollar_risk=${dollar_risk:.2f} "
                    f"({dollar_risk / portfolio_value * 100:.2f}% of portfolio)"
                )

        except Exception as e:
            log.error(f"{symbol}: {e}")


if __name__ == "__main__":
    run()
