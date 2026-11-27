# s8842 - S8842-PDHLBreakDay-H2: Close breaks yesterday's high (low) while today is up (down) from its open -> go with it.
# Weekly batch 27 Nov 2026 for BOT_PAPER (paper first, promoted only if it wins). Trades of 1-4 hours (closed after 120 min at the latest).
# 2-year test (Oct 2024 - Oct 2026, costs included) - best asset: US30: y1 +2.8R / y2 +15.1R. Most other assets lose -> paper judges per asset.
import salylib as L
import s8801_weeklib as W
import s8840_week2lib as W2

NAME = "S8842-PDHLBreakDay-H2"
SL_ATR, TP_R = 1.0, 2.0
MAX_HOLD_MIN = 120


def signals_series(d):
    return W2.pdhl_break_day(d, 2.0)[0]


def sl_series(d):
    return W2.pdhl_break_day(d, 2.0)[1]
