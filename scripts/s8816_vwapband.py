# s8816 - S8816-VWAPBand-2.5: Cairo-day VWAP: close beyond the 2.5-std band, then back inside -> fade toward VWAP.
# Weekly batch 24 Nov 2026 for BOT_PAPER (paper first, promoted only if it wins). Short trades, closed after 60 min at the latest.
import salylib as L
import s8801_weeklib as W

NAME = "S8816-VWAPBand-2.5"
SL_ATR, TP_R = 1.0, 1.2
MAX_HOLD_MIN = 60


def signals_series(d):
    return W.vwap_band(d, 2.5)[0]


def sl_series(d):
    return W.vwap_band(d, 2.5)[1]
