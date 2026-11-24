# s8817 - S8817-ORB-London30-tp1: London opening range (10:00-10:30 Cairo) - first close outside within 2h -> go.
# Weekly batch 24 Nov 2026 for BOT_PAPER (paper first, promoted only if it wins). Short trades, closed after 60 min at the latest.
import salylib as L
import s8801_weeklib as W

NAME = "S8817-ORB-London30-tp1"
SL_ATR, TP_R = 1.0, 1.0
MAX_HOLD_MIN = 60


def signals_series(d):
    return W.orb(d, 600, 30, 120)[0]


def sl_series(d):
    return W.orb(d, 600, 30, 120)[1]
