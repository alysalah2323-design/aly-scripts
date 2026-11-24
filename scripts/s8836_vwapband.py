# s8836 - S8836-VWAPBand-2.0-1m: 1-minute version of the VWAP 2-std band fade.
# Weekly batch 24 Nov 2026 for BOT_PAPER (paper first, promoted only if it wins). Short trades, closed after 30 min at the latest.
import salylib as L
import s8801_weeklib as W

NAME = "S8836-VWAPBand-2.0-1m"
SL_ATR, TP_R = 1.0, 1.0
MAX_HOLD_MIN = 30
TF_MIN = 1


def signals_series(d):
    return W.vwap_band(d, 2.0)[0]


def sl_series(d):
    return W.vwap_band(d, 2.0)[1]
