# s8814 - S8814-VWAPBand-2.0: Cairo-day VWAP: close beyond the 2-std band, then back inside -> fade toward VWAP.
# Weekly batch 24 Nov 2026 for BOT_PAPER (paper first, promoted only if it wins). Short trades, closed after 45 min at the latest.
import salylib as L
import s8801_weeklib as W

NAME = "S8814-VWAPBand-2.0"
SL_ATR, TP_R = 1.0, 1.0
MAX_HOLD_MIN = 45


def signals_series(d):
    return W.vwap_band(d, 2.0)[0]


def sl_series(d):
    return W.vwap_band(d, 2.0)[1]
