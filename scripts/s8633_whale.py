# s8633 - S8633-WhaleStrict-ASIA: WHALE on 1-minute candles (generated 18 Nov 2026 for BOT_PAPER - paper first).
# STRICT: longer and tighter box, bigger burst -> rare but stronger entries
# Cairo window 02-08; tight box then one big 1-minute burst out of it; first signal of the Cairo day;
# stop = other side of the box, target 3.0R, closed after 45 minutes at the latest.
import salylib as L

NAME = "S8633-WhaleStrict-ASIA"
TF_MIN = 1
SL_ATR, TP_R = 1.0, 3.0
MAX_HOLD_MIN = 45
_KW = dict(n_box=15, squeeze=2.5, burst=3.0, body=0.7)


def signals_series(d):
    return L.whale(d, (120, 480), **_KW)[0]


def sl_series(d):
    return L.whale(d, (120, 480), **_KW)[1]
