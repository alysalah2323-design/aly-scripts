# s8832 - S8832-PDHLReject-tp1.5: same as s8831, target 1.5R.
# Weekly batch 24 Nov 2026 for BOT_PAPER (paper first, promoted only if it wins). Short trades, closed after 60 min at the latest.
import salylib as L
import s8801_weeklib as W

NAME = "S8832-PDHLReject-tp1.5"
SL_ATR, TP_R = 1.0, 1.5
MAX_HOLD_MIN = 60


def signals_series(d):
    return W.pdhl_reject(d)[0]


def sl_series(d):
    return W.pdhl_reject(d)[1]
