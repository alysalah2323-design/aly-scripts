# s8902 - S8902-Friend-ICT: friend's paid TradingView "ICT Entry Model - Liquidity Sweep, MSS" [LunqFX] rewritten (21 Nov 2026).
# Sweep of a pivot-8 swing with close back inside, then a structure shift (close through the pivot-3 swing) within 20 bars.
# SL = the sweep extreme (min 0.2 ATR), TP 2R, max hold 4 hours. Backtest: small edge on JP225 / USTEC 15m; on paper.
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


NAME = "S8902-Friend-ICT"
SL_ATR, TP_R = 1.0, 2.0
MAX_HOLD_MIN = 240


def _ict(d):
    """ICT Entry Model [LunqFX]: liquidity sweep of a swing (pivot 8) with close back inside, then a market-structure
    shift (close through the internal swing, pivot 3) within 20 bars -> enter. SL = sweep extreme, TP 2R, min stop 0.2 ATR.
    (The original shows a limit entry at the FVG edge; here: market entry on the next candle.)"""
    h, l, c = d["high"], d["low"], d["close"]
    n = len(c); a = atr(h, l, c, 14)
    ph, pl = pivots(h, 8, 8, True), pivots(l, 8, 8, False)
    iph, ipl = pivots(h, 3, 3, True), pivots(l, 3, 3, False)
    side = np.zeros(n, np.int8); sl = np.zeros(n)
    swH = swL = intH = intL = np.nan
    hiT = loT = False
    state = 0; dr = 0; ext = mss = np.nan; waited = 0
    for i in range(n):
        if not np.isnan(ph[i]): swH, hiT = ph[i], False
        if not np.isnan(pl[i]): swL, loT = pl[i], False
        if not np.isnan(iph[i]): intH = iph[i]
        if not np.isnan(ipl[i]): intL = ipl[i]
        if state == 0:
            if not np.isnan(swL) and not loT and l[i] < swL and c[i] > swL and not np.isnan(intH) and intH > c[i]:
                loT, state, dr, ext, mss, waited = True, 1, 1, l[i], intH, 0
            elif not np.isnan(swH) and not hiT and h[i] > swH and c[i] < swH and not np.isnan(intL) and intL < c[i]:
                hiT, state, dr, ext, mss, waited = True, 1, -1, h[i], intL, 0
            continue
        waited += 1
        if waited > 20:
            state = 0; continue
        if (dr == 1 and c[i] > mss) or (dr == -1 and c[i] < mss):
            risk = abs(c[i] - ext)
            if not np.isnan(a[i]) and risk >= 0.2 * a[i]:
                side[i] = dr; sl[i] = risk
            state = 0
    return side, sl, 2.0


def signals_series(d):
    return _ict(d)[0]


def sl_series(d):
    return _ict(d)[1]
