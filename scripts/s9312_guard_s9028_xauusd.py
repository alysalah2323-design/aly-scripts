# S9312-GUARD-S9028-FastKELT4T15-XAUUSD: crazy-day GUARD on paper (22 Nov 2026). Original: S9028-FastKELT-4-T15 on XAUUSD.
# Trades only on XAUUSD, only in the first 2 hours after the session open, only in a "crazy week"
# (last 5 days' range >= 1.3 x the last 20 days). Signals, stop and target come from the original script.
import numpy as np
import s9300_guardlib as G

_O = G.load_original("S9028-FastKELT-4-T15")
NAME = "S9312-GUARD-S9028-FastKELT4T15-XAUUSD"
SL_ATR = float(getattr(_O, "SL_ATR", 1.0)) if _O else 1.0
TP_R = float(getattr(_O, "TP_R", 1.5)) if _O else 1.5
MAX_HOLD_MIN = int(getattr(_O, "MAX_HOLD_MIN", 240) or 240) if _O else 240
ASSET = "XAUUSD"


def signals_series(d):
    n = len(d["close"])
    if _O is None or not str(d.get("symbol", "")).upper().startswith(ASSET):
        return np.zeros(n, np.int8)
    s = np.nan_to_num(np.asarray(_O.signals_series(d), float)).astype(np.int8)
    return np.where(G.guard_mask(d), s, 0).astype(np.int8)


if _O is not None and hasattr(_O, "sl_series"):
    def sl_series(d):
        return _O.sl_series(d)
