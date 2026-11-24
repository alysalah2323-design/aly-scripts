# s8837 - S8837-VPFade-Roll120-1m: 1-minute version: fade back into the value area of the last 120 minutes.
# Weekly batch 24 Nov 2026 for BOT_PAPER (paper first, promoted only if it wins). Short trades, closed after 30 min at the latest.
import salylib as L
import s8801_weeklib as W

NAME = "S8837-VPFade-Roll120-1m"
SL_ATR, TP_R = 1.0, 1.0
MAX_HOLD_MIN = 30
TF_MIN = 1


def signals_series(d):
    return W.vp_fade(d, *W.rolling_profile(d, 120, 10))[0]


def sl_series(d):
    return W.vp_fade(d, *W.rolling_profile(d, 120, 10))[1]
