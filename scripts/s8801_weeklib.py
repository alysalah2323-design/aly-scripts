# s8801_weeklib.py - helpers for the 24 Nov 2026 weekly batch (volume profile, VWAP bands, ORB, RSI2, squeeze ...).
# Only numpy + salylib. Not a script itself (file name ends with "lib"). Every helper uses ONLY past/current candles.
import numpy as np
import salylib as L


def base(d):
    o, h, l, c, t = L._arrays(d)
    v = np.asarray(d.get("volume", np.ones(len(c))), float)
    v = np.where(np.isfinite(v) & (v > 0), v, 1.0)
    a = L._roll_mean(L._true_range(h, l, c), 14)
    return o, h, l, c, t, v, a


def one_per_setup(sig):
    prev = np.r_[0, sig[:-1]]
    return np.where(sig == prev, 0, sig).astype(np.int8)


def finish(sig, sl, a, min_atr=0.3):
    sig = one_per_setup(np.asarray(sig, np.int8))
    sig[~np.isfinite(a)] = 0
    with np.errstate(invalid="ignore"):
        sl = np.where(np.isfinite(sl) & (sl >= min_atr * a), sl, min_atr * a)
    return sig, sl


def profile(tp, vol, bins=24):
    """POC, VAH, VAL (70% value area) of a set of candles (typical price + volume)."""
    lo, hi = float(tp.min()), float(tp.max())
    if not (hi > lo):
        return lo, lo, lo
    edges = np.linspace(lo, hi, bins + 1)
    hist, _ = np.histogram(tp, edges, weights=vol)
    ctr = (edges[:-1] + edges[1:]) / 2
    p = int(hist.argmax()); tot = hist.sum(); s = hist[p]; a = b = p
    while s < 0.7 * tot and (a > 0 or b < bins - 1):
        up = hist[b + 1] if b < bins - 1 else -1
        dn = hist[a - 1] if a > 0 else -1
        if up >= dn:
            b += 1; s += hist[b]
        else:
            a -= 1; s += hist[a]
    step = (hi - lo) / bins
    return ctr[p], ctr[b] + step / 2, ctr[a] - step / 2


def prev_day_profile(d):
    """per candle: POC / VAH / VAL of the PREVIOUS Cairo day (NaN on the first day)."""
    o, h, l, c, t, v, a = base(d)
    mod, day = L.cairo_minutes(t)
    tp = (h + l + c) / 3
    n = len(c); P = np.full(n, np.nan); H = np.full(n, np.nan); Lo = np.full(n, np.nan)
    st = np.r_[0, np.flatnonzero(np.diff(day)) + 1]; en = np.r_[st[1:], n]
    last = None
    for s, e in zip(st, en):
        if last is not None:
            P[s:e], H[s:e], Lo[s:e] = last
        if e - s >= 8:
            last = profile(tp[s:e], v[s:e])
    return P, H, Lo


def rolling_profile(d, N, step=4):
    """POC / VAH / VAL of the last N candles BEFORE each candle (recomputed every `step` candles, from older data only)."""
    o, h, l, c, t, v, a = base(d)
    tp = (h + l + c) / 3
    n = len(c); P = np.full(n, np.nan); H = np.full(n, np.nan); Lo = np.full(n, np.nan)
    cur = None
    for i in range(N, n):
        if (i - N) % step == 0:
            cur = profile(tp[i - N:i], v[i - N:i])
        P[i], H[i], Lo[i] = cur
    return P, H, Lo


# ---------------------------------------------------------------- VOLUME PROFILE setups
def vp_fade(d, P, H, Lo, wick=0.0):
    """price pokes above VAH (below VAL) and closes back inside -> fade back into value. Stop beyond the poke."""
    o, h, l, c, t, v, a = base(d)
    with np.errstate(invalid="ignore"):
        sell = (h > H + wick * a) & (c < H) & (c > P)
        buy = (l < Lo - wick * a) & (c > Lo) & (c < P)
    sig = np.where(buy, 1, np.where(sell, -1, 0))
    sl = np.where(sig == 1, c - l + 0.1 * a, h - c + 0.1 * a)
    return finish(sig, sl, a)


def vp_break_hold(d, P, H, Lo, k=2):
    """k closes in a row outside the value area (after being inside before) -> trade the break."""
    o, h, l, c, t, v, a = base(d)
    up = np.ones(len(c), bool); dn = np.ones(len(c), bool)
    with np.errstate(invalid="ignore"):
        for j in range(k):
            cj = L._shift(c, j) if j else c
            up &= cj > H; dn &= cj < Lo
        ck = L._shift(c, k)
        up &= ck <= H; dn &= ck >= Lo
    sig = np.where(up, 1, np.where(dn, -1, 0))
    sl = np.where(sig == 1, c - np.minimum(L._roll_min(l, k), H) + 0.1 * a, np.maximum(L._roll_max(h, k), Lo) - c + 0.1 * a)
    return finish(sig, sl, a, 0.5)


def vp_to_poc(d, P, far=1.5):
    """price far (> far ATR) from the POC and a candle closing back toward it (strong body) -> go to the POC."""
    o, h, l, c, t, v, a = base(d)
    with np.errstate(invalid="ignore"):
        body = np.abs(c - o) / np.maximum(h - l, 1e-12)
        buy = (c < P - far * a) & (c > o) & (body >= 0.5) & (L._shift(c) < L._shift(o))
        sell = (c > P + far * a) & (c < o) & (body >= 0.5) & (L._shift(c) > L._shift(o))
    sig = np.where(buy, 1, np.where(sell, -1, 0))
    sl = np.where(sig == 1, c - L._roll_min(l, 3) + 0.1 * a, L._roll_max(h, 3) - c + 0.1 * a)
    return finish(sig, sl, a, 0.5)


# ---------------------------------------------------------------- OTHER setups
def vwap_band(d, k=2.0):
    """Cairo-day VWAP with std bands: close beyond the band then back inside -> fade toward VWAP."""
    o, h, l, c, t, v, a = base(d)
    mod, day = L.cairo_minutes(t)
    tp = (h + l + c) / 3
    n = len(c); vw = np.full(n, np.nan); sd = np.full(n, np.nan)
    st = np.r_[0, np.flatnonzero(np.diff(day)) + 1]; en = np.r_[st[1:], n]
    for s, e in zip(st, en):
        cv = np.cumsum(v[s:e]); m = np.cumsum(v[s:e] * tp[s:e]) / cv
        m2 = np.cumsum(v[s:e] * tp[s:e] ** 2) / cv
        vw[s:e] = m; sd[s:e] = np.sqrt(np.maximum(m2 - m * m, 0))
        vw[s:s + 4] = np.nan
    up, dn = vw + k * sd, vw - k * sd
    with np.errstate(invalid="ignore"):
        sell = (L._shift(c) > L._shift(up)) & (c < up) & (c > vw)
        buy = (L._shift(c) < L._shift(dn)) & (c > dn) & (c < vw)
    sig = np.where(buy, 1, np.where(sell, -1, 0))
    sl = np.where(sig == 1, c - L._roll_min(l, 2) + 0.1 * a, L._roll_max(h, 2) - c + 0.1 * a)
    return finish(sig, sl, a)


def orb(d, start_min, len_min=30, until_min=120):
    """Opening range of `len_min` minutes from Cairo minute `start_min`; first close outside it within `until_min` -> go."""
    o, h, l, c, t, v, a = base(d)
    mod, day = L.cairo_minutes(t)
    tf = int(d.get("tf", 15)) if np.isscalar(d.get("tf", 15)) else 15
    n = len(c); sig = np.zeros(n, np.int8); sl = np.full(n, np.nan)
    cur = None; rh = rl = None; used = False
    for i in range(n):
        if day[i] != cur:
            cur, rh, rl, used = day[i], -np.inf, np.inf, False
        m = mod[i]
        if start_min <= m and m + tf <= start_min + len_min:
            rh = max(rh, h[i]); rl = min(rl, l[i]); continue
        if used or not np.isfinite(rh) or not (start_min + len_min <= m < start_min + until_min) or not np.isfinite(a[i]):
            continue
        if c[i] > rh:
            sig[i], sl[i], used = 1, max(c[i] - (rh + rl) / 2, 0.3 * a[i]), True
        elif c[i] < rl:
            sig[i], sl[i], used = -1, max((rh + rl) / 2 - c[i], 0.3 * a[i]), True
    return sig, sl


def rsi(c, n):
    dlt = np.diff(c, prepend=c[0])
    up = np.where(dlt > 0, dlt, 0.0); dn = np.where(dlt < 0, -dlt, 0.0)
    au = np.zeros(len(c)); ad = np.zeros(len(c))
    au[0], ad[0] = up[0], dn[0]
    for i in range(1, len(c)):
        au[i] = (au[i - 1] * (n - 1) + up[i]) / n; ad[i] = (ad[i - 1] * (n - 1) + dn[i]) / n
    r = 100 - 100 / (1 + au / np.maximum(ad, 1e-12))
    r[:n + 2] = np.nan
    return r


def ema(x, n):
    out = np.empty(len(x)); k = 2 / (n + 1); out[0] = x[0]
    for i in range(1, len(x)):
        out[i] = out[i - 1] + k * (x[i] - out[i - 1])
    out[:n] = np.nan
    return out


def rsi2_trend(d, lo=10, hi=90, trend=50):
    """Connors-style: RSI(2) very low in an up-trend (close > EMA) -> buy the dip; mirror for sell."""
    o, h, l, c, t, v, a = base(d)
    r = rsi(c, 2); e = ema(c, trend)
    with np.errstate(invalid="ignore"):
        buy = (r < lo) & (c > e); sell = (r > hi) & (c < e)
    sig = np.where(buy, 1, np.where(sell, -1, 0))
    return finish(sig, np.full(len(c), np.nan), a, 1.0)


def squeeze_release(d, n=20, kc=1.5):
    """Bollinger inside Keltner (squeeze) for 3+ candles, then a close outside the Bollinger band -> go with it."""
    o, h, l, c, t, v, a = base(d)
    m = L._roll_mean(c, n)
    sd = np.sqrt(np.maximum(L._roll_mean(c * c, n) - m * m, 0))
    with np.errstate(invalid="ignore"):
        sq = (m + 2 * sd < m + kc * a) & (m - 2 * sd > m - kc * a)
        was = L._shift(sq.astype(float)) + L._shift(sq.astype(float), 2) + L._shift(sq.astype(float), 3) >= 3
        buy = was & (c > m + 2 * sd); sell = was & (c < m - 2 * sd)
    sig = np.where(buy, 1, np.where(sell, -1, 0))
    sl = np.where(sig == 1, c - m, m - c)
    return finish(sig, sl, a, 0.5)


def vol_exhaust(d, mult=3.0, wick=0.5):
    """volume >= mult x its 20-candle average with a long wick against the move -> fade (exhaustion)."""
    o, h, l, c, t, v, a = base(d)
    av = L._shift(L._roll_mean(v, 20))
    rng = np.maximum(h - l, 1e-12)
    with np.errstate(invalid="ignore"):
        big = v >= mult * av
        sell = big & ((h - np.maximum(o, c)) / rng >= wick) & (h >= L._shift(L._roll_max(h, 10)))
        buy = big & ((np.minimum(o, c) - l) / rng >= wick) & (l <= L._shift(L._roll_min(l, 10)))
    sig = np.where(buy, 1, np.where(sell, -1, 0))
    sl = np.where(sig == 1, c - l + 0.1 * a, h - c + 0.1 * a)
    return finish(sig, sl, a)


def inside_vol(d, mult=1.5):
    """inside candle, then the next candle closes beyond the mother candle with volume >= mult x average -> go."""
    o, h, l, c, t, v, a = base(d)
    av = L._shift(L._roll_mean(v, 20))
    mh, ml = L._shift(h, 2), L._shift(l, 2)
    with np.errstate(invalid="ignore"):
        ins = (L._shift(h) <= mh) & (L._shift(l) >= ml)
        buy = ins & (c > mh) & (v >= mult * av); sell = ins & (c < ml) & (v >= mult * av)
    sig = np.where(buy, 1, np.where(sell, -1, 0))
    sl = np.where(sig == 1, c - ml, mh - c)
    return finish(sig, sl, a, 0.5)


def pdhl_reject(d):
    """first poke of the previous Cairo day's high (low) that closes back inside -> fade."""
    o, h, l, c, t, v, a = base(d)
    mod, day = L.cairo_minutes(t)
    n = len(c); sig = np.zeros(n, np.int8); sl = np.full(n, np.nan)
    st = np.r_[0, np.flatnonzero(np.diff(day)) + 1]; en = np.r_[st[1:], n]
    ph = pl = None
    for s, e in zip(st, en):
        if ph is not None:
            used = False
            for i in range(s, e):
                if used or not np.isfinite(a[i]):
                    continue
                if h[i] > ph and c[i] < ph:
                    sig[i], sl[i], used = -1, h[i] - c[i] + 0.1 * a[i], True
                elif l[i] < pl and c[i] > pl:
                    sig[i], sl[i], used = 1, c[i] - l[i] + 0.1 * a[i], True
        if e - s >= 8:
            ph, pl = h[s:e].max(), l[s:e].min()
    return finish(sig, sl, a)


def three_bar_rev(d, vmult=1.2):
    """two candles one way, then an engulfing candle the other way with above-average volume -> reversal."""
    o, h, l, c, t, v, a = base(d)
    av = L._shift(L._roll_mean(v, 20))
    c1, o1, c2, o2 = L._shift(c), L._shift(o), L._shift(c, 2), L._shift(o, 2)
    with np.errstate(invalid="ignore"):
        buy = (c2 < o2) & (c1 < o1) & (c > o) & (c > o1) & (v >= vmult * av)
        sell = (c2 > o2) & (c1 > o1) & (c < o) & (c < o1) & (v >= vmult * av)
    sig = np.where(buy, 1, np.where(sell, -1, 0))
    sl = np.where(sig == 1, c - L._roll_min(l, 3) + 0.1 * a, L._roll_max(h, 3) - c + 0.1 * a)
    return finish(sig, sl, a)


def donchian_vol(d, n=20, vmult=1.3):
    """close above the n-candle high (below the low) with volume above average -> momentum break."""
    o, h, l, c, t, v, a = base(d)
    av = L._shift(L._roll_mean(v, 20))
    hh, ll = L._shift(L._roll_max(h, n)), L._shift(L._roll_min(l, n))
    with np.errstate(invalid="ignore"):
        buy = (c > hh) & (v >= vmult * av); sell = (c < ll) & (v >= vmult * av)
    sig = np.where(buy, 1, np.where(sell, -1, 0))
    return finish(sig, np.full(len(c), np.nan), a, 1.0)
