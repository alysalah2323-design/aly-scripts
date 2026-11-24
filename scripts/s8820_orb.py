# s8820 - S8820-ORB-Tokyo30-tp1: Tokyo opening range (02:00-02:30 Cairo) - first close outside within 2h -> go.
# Weekly batch 24 Nov 2026 for BOT_PAPER (paper first, promoted only if it wins). Short trades, closed after 60 min at the latest.
import salylib as L
import s8801_weeklib as W

NAME = "S8820-ORB-Tokyo30-tp1"
SL_ATR, TP_R = 1.0, 1.0
MAX_HOLD_MIN = 60


def signals_series(d):
    return W.orb(d, 120, 30, 120)[0]


def sl_series(d):
    return W.orb(d, 120, 30, 120)[1]
