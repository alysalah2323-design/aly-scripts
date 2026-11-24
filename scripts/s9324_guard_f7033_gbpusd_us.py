# S9324-GUARD-F7033-GBPUSD-US: session GUARD on paper (24 Nov 2026). Original: F7033-PivotSource on GBPUSD.
# Trades only on GBPUSD, only US 15-23 Cairo, only in a "crazy week". Signals, stop and target from the original script.
import s9321_guardseslib as GS

_O, signals_series, _sl = GS.make("F7033-PivotSource", "GBPUSD", 15, 23)
NAME = "S9324-GUARD-F7033-GBPUSD-US"
SL_ATR = float(getattr(_O, "SL_ATR", 1.0)) if _O else 1.0
TP_R = float(getattr(_O, "TP_R", 1.5)) if _O else 1.5
MAX_HOLD_MIN = int(getattr(_O, "MAX_HOLD_MIN", 240) or 240) if _O else 240
if _sl is not None:
    sl_series = _sl
