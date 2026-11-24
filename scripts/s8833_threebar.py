# s8833 - S8833-ThreeBarRevVol: 2 candles one way, then an engulfing candle the other way with volume -> reversal.
# Weekly batch 24 Nov 2026 for BOT_PAPER (paper first, promoted only if it wins). Short trades, closed after 45 min at the latest.
import salylib as L
import s8801_weeklib as W

NAME = "S8833-ThreeBarRevVol"
SL_ATR, TP_R = 1.0, 1.0
MAX_HOLD_MIN = 45


def signals_series(d):
    return W.three_bar_rev(d, 1.2)[0]


def sl_series(d):
    return W.three_bar_rev(d, 1.2)[1]
