# S9323-GUARD-F7033-BTCUSD-LONDON: session GUARD on paper (24 Nov 2026). Original: F7033-PivotSource on BTCUSD.
# Trades only on BTCUSD, only LONDON 09-15 Cairo, only in a "crazy week". Signals, stop and target from the original script.
import s9321_guardseslib as GS

_O, signals_series, _sl = GS.make("F7033-PivotSource", "BTCUSD", 9, 15)
NAME = "S9323-GUARD-F7033-BTCUSD-LONDON"
SL_ATR = float(getattr(_O, "SL_ATR", 1.0)) if _O else 1.0
TP_R = float(getattr(_O, "TP_R", 1.5)) if _O else 1.5
MAX_HOLD_MIN = int(getattr(_O, "MAX_HOLD_MIN", 240) or 240) if _O else 240
if _sl is not None:
    sl_series = _sl
