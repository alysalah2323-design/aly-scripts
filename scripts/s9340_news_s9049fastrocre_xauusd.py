# S9340-NEWS-S9049FastROCRE-XAUUSD: NEWS GUARD on paper (25 Nov 2026). Original: S9049-FastROCREV-1-T15 on XAUUSD (backtest at news: +0.24/+0.43R year1/year2,
# not proven against luck). Trades ONLY on XAUUSD, ONLY from 15 min before to 60 min after US CPI / NFP / FOMC.
import s9330_newslib as NW

_O, signals_series, _sl = NW.make("S9049-FastROCREV-1-T15", "XAUUSD")
NAME = "S9340-NEWS-S9049FastROCRE-XAUUSD"
SL_ATR = float(getattr(_O, "SL_ATR", 1.0)) if _O else 1.0
TP_R = float(getattr(_O, "TP_R", 1.5)) if _O else 1.5
MAX_HOLD_MIN = int(getattr(_O, "MAX_HOLD_MIN", 240) or 240) if _O else 240
if _sl is not None:
    sl_series = _sl
