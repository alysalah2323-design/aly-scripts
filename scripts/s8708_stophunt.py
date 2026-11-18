# s8708 - S8708-StopHunt-4h-k2-tp2: STOP HUNT / fake breakout on 15-minute candles (generated 18 Nov 2026 for BOT_PAPER).
# Price breaks the 4h high (low) and within 2 candle(s) closes back inside -> the break was a trap: trade the
# other way. Stop beyond the trap's extreme (+0.1 ATR), target 2R, closed after 60 minutes at the latest (short).
import salylib as L

NAME = "S8708-StopHunt-4h-k2-tp2"
SL_ATR, TP_R = 1.0, 2.0
MAX_HOLD_MIN = 60


def signals_series(d):
    return L.stop_hunt(d, 16, 2)[0]


def sl_series(d):
    return L.stop_hunt(d, 16, 2)[1]
