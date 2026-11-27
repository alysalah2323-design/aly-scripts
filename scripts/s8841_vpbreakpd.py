# s8841 - S8841-VPBreakPD-H4: Break out of yesterday's value area (volume profile) and hold 2 candles -> go with it.
# Weekly batch 27 Nov 2026 for BOT_PAPER (paper first, promoted only if it wins). Trades of 1-4 hours (closed after 240 min at the latest).
# 2-year test (Oct 2024 - Oct 2026, costs included) - best asset: gold: y1 +25.6R / y2 +24.1R (918 trades, +0.05R each). Most other assets lose -> paper judges per asset.
import salylib as L
import s8801_weeklib as W
import s8840_week2lib as W2

NAME = "S8841-VPBreakPD-H4"
SL_ATR, TP_R = 1.0, 2.0
MAX_HOLD_MIN = 240


def signals_series(d):
    sig, _ = W.vp_break_hold(d, *W.prev_day_profile(d))
    return sig


def sl_series(d):
    o, h, l, c, t, v, a = W.base(d)
    return 1.5 * a
