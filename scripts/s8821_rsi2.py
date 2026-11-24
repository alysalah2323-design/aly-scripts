# s8821 - S8821-RSI2-Trend-10-90: Connors RSI(2) < 10 in an up-trend (close > EMA50) -> buy the dip; mirror for sell.
# Weekly batch 24 Nov 2026 for BOT_PAPER (paper first, promoted only if it wins). Short trades, closed after 60 min at the latest.
import salylib as L
import s8801_weeklib as W

NAME = "S8821-RSI2-Trend-10-90"
SL_ATR, TP_R = 1.0, 1.0
MAX_HOLD_MIN = 60


def signals_series(d):
    return W.rsi2_trend(d, 10, 90, 50)[0]


def sl_series(d):
    return W.rsi2_trend(d, 10, 90, 50)[1]
