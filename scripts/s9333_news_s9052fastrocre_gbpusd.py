# S9333-NEWS-S9052FastROCRE-GBPUSD: NEWS GUARD on paper (25 Nov 2026). Original: S9052-FastROCREV-4-T15 on GBPUSD (backtest at news: +0.45/+0.36R year1/year2,
# not proven against luck). Trades ONLY on GBPUSD, ONLY from 15 min before to 60 min after US CPI / NFP / FOMC.
import s9330_newslib as NW

_O, signals_series, _sl = NW.make("S9052-FastROCREV-4-T15", "GBPUSD")
NAME = "S9333-NEWS-S9052FastROCRE-GBPUSD"
SL_ATR = float(getattr(_O, "SL_ATR", 1.0)) if _O else 1.0
TP_R = float(getattr(_O, "TP_R", 1.5)) if _O else 1.5
MAX_HOLD_MIN = int(getattr(_O, "MAX_HOLD_MIN", 240) or 240) if _O else 240
if _sl is not None:
    sl_series = _sl
