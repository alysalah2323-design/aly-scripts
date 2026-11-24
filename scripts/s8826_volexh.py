# s8826 - S8826-VolExhaust-3x: volume 3x average + long wick at a 10-candle extreme -> fade the exhaustion.
# Weekly batch 24 Nov 2026 for BOT_PAPER (paper first, promoted only if it wins). Short trades, closed after 45 min at the latest.
import salylib as L
import s8801_weeklib as W

NAME = "S8826-VolExhaust-3x"
SL_ATR, TP_R = 1.0, 1.0
MAX_HOLD_MIN = 45


def signals_series(d):
    return W.vol_exhaust(d, 3.0, 0.5)[0]


def sl_series(d):
    return W.vol_exhaust(d, 3.0, 0.5)[1]
