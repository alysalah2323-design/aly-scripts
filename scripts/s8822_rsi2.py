# s8822 - S8822-RSI2-Trend-5-95: RSI(2) < 5 in an up-trend (EMA50) -> buy the dip; mirror.
# Weekly batch 24 Nov 2026 for BOT_PAPER (paper first, promoted only if it wins). Short trades, closed after 60 min at the latest.
import salylib as L
import s8801_weeklib as W

NAME = "S8822-RSI2-Trend-5-95"
SL_ATR, TP_R = 1.0, 1.2
MAX_HOLD_MIN = 60


def signals_series(d):
    return W.rsi2_trend(d, 5, 95, 50)[0]


def sl_series(d):
    return W.rsi2_trend(d, 5, 95, 50)[1]
