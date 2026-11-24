# s8835 - S8835-DonchianVol-40: close above the 40-candle high (below low) with volume 1.5x average -> momentum.
# Weekly batch 24 Nov 2026 for BOT_PAPER (paper first, promoted only if it wins). Short trades, closed after 60 min at the latest.
import salylib as L
import s8801_weeklib as W

NAME = "S8835-DonchianVol-40"
SL_ATR, TP_R = 1.0, 1.5
MAX_HOLD_MIN = 60


def signals_series(d):
    return W.donchian_vol(d, 40, 1.5)[0]


def sl_series(d):
    return W.donchian_vol(d, 40, 1.5)[1]
