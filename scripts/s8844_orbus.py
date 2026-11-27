# s8844 - S8844-ORB-US30-H2: US open range (16:30-17:00 Cairo): first close outside within 3h -> go, stop 2 ATR.
# Weekly batch 27 Nov 2026 for BOT_PAPER (paper first, promoted only if it wins). Trades of 1-4 hours (closed after 120 min at the latest).
# 2-year test (Oct 2024 - Oct 2026, costs included) - best asset: BTC: y1 +6.9R / y2 +9.8R. Most other assets lose -> paper judges per asset.
import salylib as L
import s8801_weeklib as W
import s8840_week2lib as W2

NAME = "S8844-ORB-US30-H2"
SL_ATR, TP_R = 1.0, 2.0
MAX_HOLD_MIN = 120


def signals_series(d):
    return W.orb(d, 990, 30, 180)[0]


def sl_series(d):
    o, h, l, c, t, v, a = W.base(d)
    return 2.0 * a
