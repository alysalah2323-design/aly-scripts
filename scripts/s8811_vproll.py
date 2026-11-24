# s8811 - S8811-VPFade-Roll96: fade back into the value area of the last 96 candles (rolling volume profile).
# Weekly batch 24 Nov 2026 for BOT_PAPER (paper first, promoted only if it wins). Short trades, closed after 60 min at the latest.
import salylib as L
import s8801_weeklib as W

NAME = "S8811-VPFade-Roll96"
SL_ATR, TP_R = 1.0, 1.2
MAX_HOLD_MIN = 60


def signals_series(d):
    return W.vp_fade(d, *W.rolling_profile(d, 96))[0]


def sl_series(d):
    return W.vp_fade(d, *W.rolling_profile(d, 96))[1]
