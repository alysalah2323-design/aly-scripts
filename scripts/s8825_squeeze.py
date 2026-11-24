# s8825 - S8825-SqueezeRelease-20-2.0: looser squeeze (Keltner 2.0 ATR), then a close outside Bollinger -> go.
# Weekly batch 24 Nov 2026 for BOT_PAPER (paper first, promoted only if it wins). Short trades, closed after 60 min at the latest.
import salylib as L
import s8801_weeklib as W

NAME = "S8825-SqueezeRelease-20-2.0"
SL_ATR, TP_R = 1.0, 1.2
MAX_HOLD_MIN = 60


def signals_series(d):
    return W.squeeze_release(d, 20, 2.0)[0]


def sl_series(d):
    return W.squeeze_release(d, 20, 2.0)[1]
