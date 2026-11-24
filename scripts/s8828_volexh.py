# s8828 - S8828-VolExhaust-2.5x-w0.4: volume 2.5x average + wick >= 40% at a 10-candle extreme -> fade.
# Weekly batch 24 Nov 2026 for BOT_PAPER (paper first, promoted only if it wins). Short trades, closed after 60 min at the latest.
import salylib as L
import s8801_weeklib as W

NAME = "S8828-VolExhaust-2.5x-w0.4"
SL_ATR, TP_R = 1.0, 1.2
MAX_HOLD_MIN = 60


def signals_series(d):
    return W.vol_exhaust(d, 2.5, 0.4)[0]


def sl_series(d):
    return W.vol_exhaust(d, 2.5, 0.4)[1]
