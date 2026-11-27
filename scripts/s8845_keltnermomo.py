# s8845 - S8845-KeltnerMomo-H4: Close beyond EMA20 +- 2 ATR while EMA50 points the same way -> momentum.
# Weekly batch 27 Nov 2026 for BOT_PAPER (paper first, promoted only if it wins). Trades of 1-4 hours (closed after 240 min at the latest).
# 2-year test (Oct 2024 - Oct 2026, costs included) - best asset: gold: y1 +13.3R / y2 +8.6R. Most other assets lose -> paper judges per asset.
import salylib as L
import s8801_weeklib as W
import s8840_week2lib as W2

NAME = "S8845-KeltnerMomo-H4"
SL_ATR, TP_R = 1.0, 2.0
MAX_HOLD_MIN = 240


def signals_series(d):
    return W2.keltner_momo(d, 2.0)[0]


def sl_series(d):
    return W2.keltner_momo(d, 2.0)[1]
