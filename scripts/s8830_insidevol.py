# s8830 - S8830-InsideBreakVol-1.2x: inside candle, then a close beyond the mother candle with volume 1.2x average -> go.
# Weekly batch 24 Nov 2026 for BOT_PAPER (paper first, promoted only if it wins). Short trades, closed after 45 min at the latest.
import salylib as L
import s8801_weeklib as W

NAME = "S8830-InsideBreakVol-1.2x"
SL_ATR, TP_R = 1.0, 1.0
MAX_HOLD_MIN = 45


def signals_series(d):
    return W.inside_vol(d, 1.2)[0]


def sl_series(d):
    return W.inside_vol(d, 1.2)[1]
