# s8823 - S8823-RSI2-Trend-15-85-E100: RSI(2) < 15 in an up-trend (EMA100) -> buy the dip; mirror.
# Weekly batch 24 Nov 2026 for BOT_PAPER (paper first, promoted only if it wins). Short trades, closed after 45 min at the latest.
import salylib as L
import s8801_weeklib as W

NAME = "S8823-RSI2-Trend-15-85-E100"
SL_ATR, TP_R = 1.0, 1.0
MAX_HOLD_MIN = 45


def signals_series(d):
    return W.rsi2_trend(d, 15, 85, 100)[0]


def sl_series(d):
    return W.rsi2_trend(d, 15, 85, 100)[1]
