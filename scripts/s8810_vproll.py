# s8810 - S8810-VPFade-Roll48: fade back into the value area of the last 48 candles (rolling volume profile).
# Weekly batch 24 Nov 2026 for BOT_PAPER (paper first, promoted only if it wins). Short trades, closed after 45 min at the latest.
import salylib as L
import s8801_weeklib as W

NAME = "S8810-VPFade-Roll48"
SL_ATR, TP_R = 1.0, 1.0
MAX_HOLD_MIN = 45


def signals_series(d):
    return W.vp_fade(d, *W.rolling_profile(d, 48))[0]


def sl_series(d):
    return W.vp_fade(d, *W.rolling_profile(d, 48))[1]
