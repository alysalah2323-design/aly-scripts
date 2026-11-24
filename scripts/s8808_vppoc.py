# s8808 - S8808-VPToPOC-PrevDay-far1.5: far (>1.5 ATR) from yesterday's POC + a strong candle back toward it -> go to the POC magnet.
# Weekly batch 24 Nov 2026 for BOT_PAPER (paper first, promoted only if it wins). Short trades, closed after 60 min at the latest.
import salylib as L
import s8801_weeklib as W

NAME = "S8808-VPToPOC-PrevDay-far1.5"
SL_ATR, TP_R = 1.0, 1.0
MAX_HOLD_MIN = 60


def signals_series(d):
    return W.vp_to_poc(d, W.prev_day_profile(d)[0], far=1.5)[0]


def sl_series(d):
    return W.vp_to_poc(d, W.prev_day_profile(d)[0], far=1.5)[1]
