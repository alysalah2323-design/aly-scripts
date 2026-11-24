# s8824 - S8824-SqueezeRelease-20-1.5: Bollinger inside Keltner 3+ candles, then a close outside Bollinger -> go with it.
# Weekly batch 24 Nov 2026 for BOT_PAPER (paper first, promoted only if it wins). Short trades, closed after 60 min at the latest.
import salylib as L
import s8801_weeklib as W

NAME = "S8824-SqueezeRelease-20-1.5"
SL_ATR, TP_R = 1.0, 1.5
MAX_HOLD_MIN = 60


def signals_series(d):
    return W.squeeze_release(d, 20, 1.5)[0]


def sl_series(d):
    return W.squeeze_release(d, 20, 1.5)[1]
