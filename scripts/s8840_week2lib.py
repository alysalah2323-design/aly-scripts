# s8840_week2lib.py - helpers for the 27 Nov 2026 weekly batch: trades of 1-4 hours (trend-day pullbacks, breakouts
# with the day, momentum, sessions). Only numpy + salylib + s8801_weeklib. Every helper uses ONLY past/current candles.
import numpy as np
import salylib as L
import s8801_weeklib as W


def ema(x, n):
    return W.ema(x, n)


def day_open(t, o):
    day = np.asarray(t, "int64") // 86400
    first = np.r_[True, day[1:] != day[:-1]]
    idx = np.maximum.accumulate(np.where(first, np.arange(len(o)), 0))
    return o[idx], first


def day_strength(d):
    """(close - today's UTC-day open) in units of 8 x the 15m ATR (about one normal day's move)."""
    o, h, l, c, t, v, a = W.base(d)
    dop, _ = day_open(t, o)
    with np.errstate(invalid="ignore", divide="ignore"):
        return (c - dop) / (8 * a)


def _out(sig, a, slm):
    sig = W.one_per_setup(np.asarray(sig, np.int8))
    sig[~np.isfinite(a)] = 0
    return sig, slm * a


def trend_day_pull(d, k=0.3, slm=1.5, n=20):
    """Strong day (moved k day-ranges from the open): price dips to the EMA(n) and closes back with the day."""
    o, h, l, c, t, v, a = W.base(d)
    st = day_strength(d); e = ema(c, n)
    with np.errstate(invalid="ignore"):
        buy = (st >= k) & (l <= e) & (c > e) & (c > o)
        sell = (st <= -k) & (h >= e) & (c < e) & (c < o)
    return _out(np.where(buy, 1, np.where(sell, -1, 0)), a, slm)


def pdhl_break_day(d, slm=1.5):
    """Close breaks yesterday's high (low) while today is up (down) from its open -> go with it."""
    o, h, l, c, t, v, a = W.base(d)
    day = np.asarray(t, "int64") // 86400
    ph = np.full(len(c), np.nan); pl = np.full(len(c), np.nan)
    st = np.r_[0, np.flatnonzero(np.diff(day)) + 1]; en = np.r_[st[1:], len(c)]
    for j in range(1, len(st)):
        ph[st[j]:en[j]] = h[st[j - 1]:en[j - 1]].max(); pl[st[j]:en[j]] = l[st[j - 1]:en[j - 1]].min()
    dop, _ = day_open(t, o)
    with np.errstate(invalid="ignore"):
        buy = (c > ph) & (L._shift(c) <= L._shift(ph)) & (c > dop)
        sell = (c < pl) & (L._shift(c) >= L._shift(pl)) & (c < dop)
    return _out(np.where(buy, 1, np.where(sell, -1, 0)), a, slm)


def ema_trend_rsi(d, slm=1.5, lo=40, hi=60):
    """EMA50 above EMA200 (15m) and RSI(14) comes back up through `lo` -> buy (mirror for sell)."""
    o, h, l, c, t, v, a = W.base(d)
    e50, e200 = ema(c, 50), ema(c, 200); r = W.rsi(c, 14); rp = L._shift(r)
    with np.errstate(invalid="ignore"):
        buy = (e50 > e200) & (c > e200) & (rp < lo) & (r >= lo)
        sell = (e50 < e200) & (c < e200) & (rp > hi) & (r <= hi)
    return _out(np.where(buy, 1, np.where(sell, -1, 0)), a, slm)


def keltner_momo(d, slm=1.5, k=2.0):
    """Close above EMA20 + k ATR while EMA50 is rising -> momentum buy (mirror for sell)."""
    o, h, l, c, t, v, a = W.base(d)
    e20, e50 = ema(c, 20), ema(c, 50)
    with np.errstate(invalid="ignore"):
        buy = (c > e20 + k * a) & (e50 > L._shift(e50, 4))
        sell = (c < e20 - k * a) & (e50 < L._shift(e50, 4))
    return _out(np.where(buy, 1, np.where(sell, -1, 0)), a, slm)


def donch_day(d, n=40, slm=1.5):
    """Close at a new n-candle high (low) and today is up (down) from its open -> go with it."""
    o, h, l, c, t, v, a = W.base(d)
    hh = L._shift(L._roll_max(h, n)); ll = L._shift(L._roll_min(l, n)); dop, _ = day_open(t, o)
    with np.errstate(invalid="ignore"):
        buy = (c > hh) & (c > dop); sell = (c < ll) & (c < dop)
    return _out(np.where(buy, 1, np.where(sell, -1, 0)), a, slm)


def session_follow(d, start_min, len_min=60, slm=1.5, k=0.5):
    """First `len_min` minutes after Cairo minute `start_min`: if that hour moved more than k ATR, follow it once."""
    o, h, l, c, t, v, a = W.base(d)
    mod, day = L.cairo_minutes(t)
    tf = int(d.get("tf", 15)) if np.isscalar(d.get("tf", 15)) else 15
    sig = np.zeros(len(c), np.int8); cur = None; px = None; done = False
    for i in range(len(c)):
        if day[i] != cur:
            cur, px, done = day[i], None, False
        m = mod[i]
        if m == start_min:
            px = o[i]
        if px is not None and not done and m + tf == start_min + len_min and np.isfinite(a[i]):
            mv = c[i] - px
            if mv > k * a[i]: sig[i] = 1
            elif mv < -k * a[i]: sig[i] = -1
            done = True
    return sig, slm * a
