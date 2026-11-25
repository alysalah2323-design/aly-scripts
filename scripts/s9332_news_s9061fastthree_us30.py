# S9332-NEWS-S9061FastTHREE-US30: NEWS GUARD on paper (25 Nov 2026). Original: S9061-FastTHREE-2-T15 on US30 (backtest at news: +0.37/+0.45R year1/year2,
# not proven against luck). Trades ONLY on US30, ONLY from 15 min before to 60 min after US CPI / NFP / FOMC.
import s9330_newslib as NW

_O, signals_series, _sl = NW.make("S9061-FastTHREE-2-T15", "US30")
NAME = "S9332-NEWS-S9061FastTHREE-US30"
SL_ATR = float(getattr(_O, "SL_ATR", 1.0)) if _O else 1.0
TP_R = float(getattr(_O, "TP_R", 1.5)) if _O else 1.5
MAX_HOLD_MIN = int(getattr(_O, "MAX_HOLD_MIN", 240) or 240) if _O else 240
if _sl is not None:
    sl_series = _sl
