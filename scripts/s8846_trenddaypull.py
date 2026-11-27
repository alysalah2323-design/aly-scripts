# s8846 - S8846-TrendDayPull-H4: Strong day (0.3 day-range from the open): dip to EMA20 and close back with the day.
# Weekly batch 27 Nov 2026 for BOT_PAPER (paper first, promoted only if it wins). Trades of 1-4 hours (closed after 240 min at the latest).
# 2-year test (Oct 2024 - Oct 2026, costs included) - best asset: USTEC: y1 +5.8R / y2 +4.2R. Most other assets lose -> paper judges per asset.
import salylib as L
import s8801_weeklib as W
import s8840_week2lib as W2

NAME = "S8846-TrendDayPull-H4"
SL_ATR, TP_R = 1.0, 2.0
MAX_HOLD_MIN = 240


def signals_series(d):
    return W2.trend_day_pull(d, 0.3, 1.5)[0]


def sl_series(d):
    return W2.trend_day_pull(d, 0.3, 1.5)[1]
