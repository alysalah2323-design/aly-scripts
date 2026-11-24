# s8831 - S8831-PDHLReject: first poke of yesterday's high (low) that closes back inside -> fade.
# Weekly batch 24 Nov 2026 for BOT_PAPER (paper first, promoted only if it wins). Short trades, closed after 60 min at the latest.
import salylib as L
import s8801_weeklib as W

NAME = "S8831-PDHLReject"
SL_ATR, TP_R = 1.0, 1.0
MAX_HOLD_MIN = 60


def signals_series(d):
    return W.pdhl_reject(d)[0]


def sl_series(d):
    return W.pdhl_reject(d)[1]
