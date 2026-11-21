# s8901 - S8901-Friend-Supertrend: friend's paid TradingView "Supertrend with Entry" rewritten (21 Nov 2026).
# Supertrend factor 2.5, ATR 14; BUY/SELL on the flip; SL 1.5 ATR, TP 2R; max hold 4 hours.
# 2-year backtest (FRIEND6): best on JP225 10m/15m (both years positive, also on bad days); on paper to prove itself.
import numpy as np


def atr(h, l, c, n):
    pc = np.r_[c[0], c[:-1]]
    tr = np.maximum(h - l, np.maximum(np.abs(h - pc), np.abs(l - pc)))
    out = np.full(len(c), np.nan)
    if len(c) <= n:
        return out
    out[n - 1] = tr[:n].mean()
    for i in range(n, len(c)):
        out[i] = (out[i - 1] * (n - 1) + tr[i]) / n
    return out


def pivots(x, left, right, high=True):
    """Confirmed pivots: value at bar p, KNOWN at bar p + right. Returns array conf[i] = pivot price confirmed at bar i (nan if none)."""
    n = len(x)
    conf = np.full(n, np.nan)
    for p in range(left, n - right):
        w = x[p - left:p + right + 1]
        v = x[p]
        if high:
            if v == w.max() and (w[:left] < v).all() and (w[left + 1:] <= v).all():
                conf[p + right] = v
        else:
            if v == w.min() and (w[:left] > v).all() and (w[left + 1:] >= v).all():
                conf[p + right] = v
    return conf


# ------------------------------------------------------------------ the 6 scripts
# each returns (side[i] in {-1,0,1}, stop distance[i] in price, take-profit in R (float or array))


NAME = "S8901-Friend-Supertrend"
SL_ATR, TP_R = 1.5, 2.0
MAX_HOLD_MIN = 240


def _st(d):
    """Supertrend with Entry: Supertrend factor 2.5, ATR 14; BUY/SELL on the flip. SL 1.5 ATR, TP 2R (TP2)."""
    h, l, c = d["high"], d["low"], d["close"]
    n = len(c); a = atr(h, l, c, 14)
    hl2 = (h + l) / 2
    side = np.zeros(n, np.int8); sl = np.zeros(n)
    fu = fl = np.nan; trend = 0
    for i in range(1, n):
        if np.isnan(a[i]):
            continue
        bu, bl = hl2[i] + 2.5 * a[i], hl2[i] - 2.5 * a[i]
        nfu = bu if (np.isnan(fu) or bu < fu or c[i - 1] > fu) else fu
        nfl = bl if (np.isnan(fl) or bl > fl or c[i - 1] < fl) else fl
        prev = trend
        if trend <= 0 and not np.isnan(fu) and c[i] > fu:
            trend = 1
        elif trend >= 0 and not np.isnan(fl) and c[i] < fl:
            trend = -1
        elif trend == 0:
            trend = 1 if c[i] > hl2[i] else -1
        fu, fl = nfu, nfl
        if prev != 0 and trend != prev:
            side[i] = trend; sl[i] = 1.5 * a[i]
    return side, sl, 2.0


def signals_series(d):
    return _st(d)[0]
