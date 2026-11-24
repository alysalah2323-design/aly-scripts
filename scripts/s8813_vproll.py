# s8813 - S8813-VPToPOC-Roll64: far (>1.5 ATR) from the rolling 64-candle POC + strong candle back -> go to the POC.
# Weekly batch 24 Nov 2026 for BOT_PAPER (paper first, promoted only if it wins). Short trades, closed after 45 min at the latest.
import salylib as L
import s8801_weeklib as W

NAME = "S8813-VPToPOC-Roll64"
SL_ATR, TP_R = 1.0, 1.0
MAX_HOLD_MIN = 45


def signals_series(d):
    return W.vp_to_poc(d, W.rolling_profile(d, 64)[0], far=1.5)[0]


def sl_series(d):
    return W.vp_to_poc(d, W.rolling_profile(d, 64)[0], far=1.5)[1]
