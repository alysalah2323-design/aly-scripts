# s8829 - S8829-InsideBreakVol-1.5x: inside candle, then a close beyond the mother candle with volume 1.5x average -> go.
# Weekly batch 24 Nov 2026 for BOT_PAPER (paper first, promoted only if it wins). Short trades, closed after 60 min at the latest.
import salylib as L
import s8801_weeklib as W

NAME = "S8829-InsideBreakVol-1.5x"
SL_ATR, TP_R = 1.0, 1.2
MAX_HOLD_MIN = 60


def signals_series(d):
    return W.inside_vol(d, 1.5)[0]


def sl_series(d):
    return W.inside_vol(d, 1.5)[1]
