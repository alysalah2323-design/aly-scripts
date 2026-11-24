# s8809 - S8809-VPToPOC-PrevDay-far2.5: far (>2.5 ATR) from yesterday's naked POC + a strong candle back toward it.
# Weekly batch 24 Nov 2026 for BOT_PAPER (paper first, promoted only if it wins). Short trades, closed after 60 min at the latest.
import salylib as L
import s8801_weeklib as W

NAME = "S8809-VPToPOC-PrevDay-far2.5"
SL_ATR, TP_R = 1.0, 1.5
MAX_HOLD_MIN = 60


def signals_series(d):
    return W.vp_to_poc(d, W.prev_day_profile(d)[0], far=2.5)[0]


def sl_series(d):
    return W.vp_to_poc(d, W.prev_day_profile(d)[0], far=2.5)[1]
