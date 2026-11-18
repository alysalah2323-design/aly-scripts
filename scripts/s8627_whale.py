# s8627 - S8627-Whale-LATE-b10-h45-tp2: WHALE on 1-minute candles (generated 18 Nov 2026 for BOT_PAPER - paper first).
# standard whale (like W1/W2 on the demo)
# Cairo window 18-02; tight box then one big 1-minute burst out of it; first signal of the Cairo day;
# stop = other side of the box, target 2.0R, closed after 45 minutes at the latest.
import salylib as L

NAME = "S8627-Whale-LATE-b10-h45-tp2"
TF_MIN = 1
SL_ATR, TP_R = 1.0, 2.0
MAX_HOLD_MIN = 45
_KW = dict(n_box=10)


def signals_series(d):
    return L.whale(d, (1080, 120), **_KW)[0]


def sl_series(d):
    return L.whale(d, (1080, 120), **_KW)[1]
