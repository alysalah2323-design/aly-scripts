# s8806 - S8806-VPBreakHold-PrevDay-k1: 1 close outside the previous day's value area -> trade the break.
# Weekly batch 24 Nov 2026 for BOT_PAPER (paper first, promoted only if it wins). Short trades, closed after 45 min at the latest.
import salylib as L
import s8801_weeklib as W

NAME = "S8806-VPBreakHold-PrevDay-k1"
SL_ATR, TP_R = 1.0, 1.0
MAX_HOLD_MIN = 45


def signals_series(d):
    return W.vp_break_hold(d, *W.prev_day_profile(d), k=1)[0]


def sl_series(d):
    return W.vp_break_hold(d, *W.prev_day_profile(d), k=1)[1]
