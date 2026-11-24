# s8807 - S8807-VPBreakHold-PrevDay-k3: 3 closes in a row outside the previous day's value area -> trade the break.
# Weekly batch 24 Nov 2026 for BOT_PAPER (paper first, promoted only if it wins). Short trades, closed after 60 min at the latest.
import salylib as L
import s8801_weeklib as W

NAME = "S8807-VPBreakHold-PrevDay-k3"
SL_ATR, TP_R = 1.0, 1.5
MAX_HOLD_MIN = 60


def signals_series(d):
    return W.vp_break_hold(d, *W.prev_day_profile(d), k=3)[0]


def sl_series(d):
    return W.vp_break_hold(d, *W.prev_day_profile(d), k=3)[1]
