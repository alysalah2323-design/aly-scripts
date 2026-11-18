# salylib.py - helpers for Aly's generated library scripts (whale on 1-minute candles, stop hunt on 15-minute candles).
# Uses only numpy + the standard library. Not a script itself (file name ends with "lib").
from datetime import datetime, timezone
import numpy as np

try:
    from zoneinfo import ZoneInfo
    _CAIRO = ZoneInfo("Africa/Cairo")
except Exception:
    _CAIRO = None


def cairo_minutes(t):
    """Cairo minute-of-day and Cairo day id for unix seconds t (DST-aware, one offset per UTC day)."""
    t = np.asarray(t, "int64")
    day_utc = t // 86400
    mod = np.zeros(len(t), "int64"); dayid = np.zeros(len(t), "int64")
    for du in np.unique(day_utc):
        sel = day_utc == du
        for part in (sel & (t % 86400 < 43200), sel & (t % 86400 >= 43200)):
            if not part.any():
                continue
            t0 = int(t[part][0])
            if _CAIRO is not None:
                off = int(datetime.fromtimestamp(t0, tz=_CAIRO).utcoffset().total_seconds())
            else:
                off = 7200
            lt = t[part] + off
            mod[part] = (lt % 86400) // 60
            dayid[part] = lt // 86400
    return mod, dayid


def in_window(mod, ws, we):
    return (mod >= ws) & (mod < we) if ws < we else (mod >= ws) | (mod < we)


def _roll_max(x, n):
    out = np.full(len(x), np.nan)
    if len(x) > n:
        w = np.lib.stride_tricks.sliding_window_view(x, n)
        out[n - 1:] = w.max(axis=1)
    return out


def _roll_min(x, n):
    out = np.full(len(x), np.nan)
    if len(x) > n:
        w = np.lib.stride_tricks.sliding_window_view(x, n)
        out[n - 1:] = w.min(axis=1)
    return out


def _roll_mean(x, n):
    out = np.full(len(x), np.nan)
    if len(x) >= n:
        cs = np.cumsum(np.r_[0.0, x])
        out[n - 1:] = (cs[n:] - cs[:-n]) / n
    return out


def _shift(x, k=1):
    out = np.full(len(x), np.nan)
    out[k:] = x[:-k]
    return out


def _true_range(h, l, c):
    pc = np.r_[c[0], c[:-1]]
    return np.maximum(h, pc) - np.minimum(l, pc)


def _arrays(d):
    return (np.asarray(d["open"], float), np.asarray(d["high"], float), np.asarray(d["low"], float),
            np.asarray(d["close"], float), np.asarray(d["time"], "int64"))


# ---------------------------------------------------------------- WHALE (1-minute candles)
def whale(d, win, n_box=10, squeeze=3.0, burst=2.0, body=0.6, outer=0.25, late=3.5):
    """Tight box of n_box minutes, then one big 1-minute burst out of it, inside the Cairo window, first signal of the
    Cairo day only. Returns (signal array 1/-1/0, stop distance array = other side of the box)."""
    o, h, l, c, t = _arrays(d)
    n = len(c)
    tr = _true_range(h, l, c)
    norm = _shift(_roll_mean(tr, 60))
    bh = _shift(_roll_max(h, n_box)); bl = _shift(_roll_min(l, n_box))
    box = bh - bl
    rng = h - l; bod = np.abs(c - o)
    with np.errstate(invalid="ignore"):
        sq = (box > 0) & (box <= squeeze * norm)
        big = (rng >= burst * norm) & (bod >= body * rng)
        up = sq & big & (c > bh) & (c > o) & (h - c <= outer * rng)
        dn = sq & big & (c < bl) & (c < o) & (c - l <= outer * rng)
        a5 = _roll_mean(tr, 14) * 2.24                      # ~ 5-minute ATR from 1-minute ranges
        mid = (bh + bl) / 2
        up &= (c - mid) <= late * a5
        dn &= (mid - c) <= late * a5
    mod, day = cairo_minutes(t)
    ok = in_window(mod, win[0], win[1])
    raw = np.where(up & ok, 1, np.where(dn & ok, -1, 0))
    sig = np.zeros(n, np.int8)
    used = set()
    for i in np.flatnonzero(raw):                           # only the first signal of each Cairo day
        if day[i] in used:
            continue
        used.add(day[i]); sig[i] = raw[i]
    with np.errstate(invalid="ignore"):
        sl = np.where(raw >= 0, c - bl, bh - c)
        sl = np.where(sl > 0.2 * norm, sl, norm)
    return sig, sl


# ---------------------------------------------------------------- STOP HUNT (15-minute candles)
def stop_hunt(d, look, k=1):
    """Price breaks the high (low) of the last `look` candles, then within `k` candles closes back inside ->
    the breakout was a trap: SELL (BUY). Stop beyond the trap's extreme (+0.1 ATR, at least 0.3 ATR)."""
    o, h, l, c, t = _arrays(d)
    n = len(c)
    a = _roll_mean(_true_range(h, l, c), 14)
    sig = np.zeros(n, np.int8); sl = np.full(n, np.nan)
    hi_lvl = _shift(_roll_max(h, look)); lo_lvl = _shift(_roll_min(l, look))
    for j in range(k):                                      # the trap candle is j candles ago (0 = this candle)
        lvl_h = _shift(hi_lvl, j) if j else hi_lvl
        lvl_l = _shift(lo_lvl, j) if j else lo_lvl
        th = _shift(h, j) if j else h
        tl = _shift(l, j) if j else l
        with np.errstate(invalid="ignore"):
            sell = (th > lvl_h) & (c < lvl_h)
            buy = (tl < lvl_l) & (c > lvl_l)
            if j:                                           # the trap candle itself closed outside (a real-looking break)
                tc = _shift(c, j)
                sell &= tc > lvl_h
                buy &= tc < lvl_l
        ext_h = _roll_max(h, j + 1); ext_l = _roll_min(l, j + 1)
        new_s = sell & (sig == 0); new_b = buy & (sig == 0)
        sig[new_s] = -1; sig[new_b] = 1
        with np.errstate(invalid="ignore"):
            sl = np.where(new_s, ext_h - c + 0.1 * a, sl)
            sl = np.where(new_b, c - ext_l + 0.1 * a, sl)
    prev_sig = np.r_[0, sig[:-1]]
    sig = np.where(sig == prev_sig, 0, sig).astype(np.int8)  # one trade per trap (not on the next candle again)
    sig[~np.isfinite(a)] = 0                                 # no ATR yet (first candles) -> no trade
    with np.errstate(invalid="ignore"):
        sl = np.where(sl >= 0.3 * a, sl, 0.3 * a)
    return sig, sl


def asia_hunt(d):
    """Stop hunt of the Cairo ASIA range (00:00-09:00): during London (09:00-15:00) price breaks the Asia high/low and
    closes back inside -> trade back into the range."""
    o, h, l, c, t = _arrays(d)
    n = len(c)
    a = _roll_mean(_true_range(h, l, c), 14)
    mod, day = cairo_minutes(t)
    sig = np.zeros(n, np.int8); sl = np.full(n, np.nan)
    ah = al = None; cur = None; used = False
    for i in range(n):
        if day[i] != cur:
            cur, ah, al, used = day[i], -np.inf, np.inf, False
        if mod[i] < 540:
            ah = max(ah, h[i]); al = min(al, l[i]); continue
        if mod[i] >= 900 or used or not np.isfinite(ah) or not np.isfinite(a[i]):
            continue
        if h[i] > ah and c[i] < ah:
            sig[i], sl[i], used = -1, max(h[i] - c[i] + 0.1 * a[i], 0.3 * a[i]), True
        elif l[i] < al and c[i] > al:
            sig[i], sl[i], used = 1, max(c[i] - l[i] + 0.1 * a[i], 0.3 * a[i]), True
    return sig, sl
