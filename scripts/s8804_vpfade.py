# s8804 - S8804-VPFade-PrevDay-wick0.2: previous-day VAH/VAL fade, the poke must go 0.2 ATR beyond the edge.
# Weekly batch 24 Nov 2026 for BOT_PAPER (paper first, promoted only if it wins). Short trades, closed after 60 min at the latest.
import salylib as L
import s8801_weeklib as W

NAME = "S8804-VPFade-PrevDay-wick0.2"
SL_ATR, TP_R = 1.0, 1.2
MAX_HOLD_MIN = 60


def signals_series(d):
    return W.vp_fade(d, *W.prev_day_profile(d), wick=0.2)[0]


def sl_series(d):
    return W.vp_fade(d, *W.prev_day_profile(d), wick=0.2)[1]
