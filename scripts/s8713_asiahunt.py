# s8713 - S8713-AsiaHunt-tp1.5: STOP HUNT of the Cairo Asia range (00-09) during London (09-15), 15-minute candles
# (generated 18 Nov 2026 for BOT_PAPER). Break of the Asia high/low that closes back inside -> trade back into the
# range. Stop beyond the trap candle (+0.1 ATR), target 1.5R, closed after 60 minutes at the latest.
import salylib as L

NAME = "S8713-AsiaHunt-tp1.5"
SL_ATR, TP_R = 1.0, 1.5
MAX_HOLD_MIN = 60


def signals_series(d):
    return L.asia_hunt(d)[0]


def sl_series(d):
    return L.asia_hunt(d)[1]
