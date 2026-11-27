# s8843 - S8843-DonchDay80-H4: New 80-candle (20h) high/low on the side of today's move -> go with it.
# Weekly batch 27 Nov 2026 for BOT_PAPER (paper first, promoted only if it wins). Trades of 1-4 hours (closed after 240 min at the latest).
# 2-year test (Oct 2024 - Oct 2026, costs included) - best asset: JP225: y1 +4.3R / y2 +14.6R, also wins on back-and-forth days (+15R). Most other assets lose -> paper judges per asset.
import salylib as L
import s8801_weeklib as W
import s8840_week2lib as W2

NAME = "S8843-DonchDay80-H4"
SL_ATR, TP_R = 1.0, 2.0
MAX_HOLD_MIN = 240


def signals_series(d):
    return W2.donch_day(d, 80, 2.0)[0]


def sl_series(d):
    return W2.donch_day(d, 80, 2.0)[1]
