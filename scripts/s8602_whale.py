# s8602 - S8602-Whale-ASIA-b10-h30-tp3: WHALE on 1-minute candles (generated 18 Nov 2026 for BOT_PAPER - paper first).
# standard whale (like W1/W2 on the demo)
# Cairo window 02-08; tight box then one big 1-minute burst out of it; first signal of the Cairo day;
# stop = other side of the box, target 3.0R, closed after 30 minutes at the latest.
import salylib as L

NAME = "S8602-Whale-ASIA-b10-h30-tp3"
TF_MIN = 1
SL_ATR, TP_R = 1.0, 3.0
MAX_HOLD_MIN = 30
_KW = dict(n_box=10)


def signals_series(d):
    return L.whale(d, (120, 480), **_KW)[0]


def sl_series(d):
    return L.whale(d, (120, 480), **_KW)[1]
