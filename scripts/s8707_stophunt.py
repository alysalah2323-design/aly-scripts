# s8707 - S8707-StopHunt-4h-k2-tp1.5: STOP HUNT / fake breakout on 15-minute candles (generated 18 Nov 2026 for BOT_PAPER).
# Price breaks the 4h high (low) and within 2 candle(s) closes back inside -> the break was a trap: trade the
# other way. Stop beyond the trap's extreme (+0.1 ATR), target 1.5R, closed after 60 minutes at the latest (short).
import salylib as L

NAME = "S8707-StopHunt-4h-k2-tp1.5"
SL_ATR, TP_R = 1.0, 1.5
MAX_HOLD_MIN = 60


def signals_series(d):
    return L.stop_hunt(d, 16, 2)[0]


def sl_series(d):
    return L.stop_hunt(d, 16, 2)[1]
