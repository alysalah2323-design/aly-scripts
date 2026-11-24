# F7008-ZaratustraV17 in plain numpy (24 Nov 2026) - same entry rules as the Freqtrade strategy ZaratustraV17
# (ta-lib ADX / DX / +DI / -DI 14, LINEARREG_SLOPE 14, TSF 14, Bollinger 8 x 2 on the typical price), so it runs on the
# VPS without Freqtrade / ta-lib. Used by the crazy-day guard S9320 (JP225). Exits = our stop / target.
#   LONG  when the slope is > 0 and rising, AND (close crosses above the upper Bollinger band, OR close crosses above
#         the TSF line, OR DX > -DI and ADX > -DI and +DI > -DI).  SHORT = mirror.
import numpy as np

NAME = "F7008-ZaratustraV17"
SL_ATR, TP_R = 1.0, 1.0
N = 14


def _wilder(x, n):
    out = np.full(len(x), np.nan)
    if len(x) <= n:
        return out
    s = np.nansum(x[1:n])                           # ta-lib: start from the sum of the first n-1 moves
    for i in range(n, len(x)):
        s = s - s / n + x[i]
        out[i] = s
    return out


def _dmi(h, l, c, n=N):
    up = np.r_[np.nan, h[1:] - h[:-1]]; dn = np.r_[np.nan, l[:-1] - l[1:]]
    pdm = np.where((up > dn) & (up > 0), up, 0.0); mdm = np.where((dn > up) & (dn > 0), dn, 0.0)
    pc = np.r_[np.nan, c[:-1]]
    tr = np.nanmax(np.vstack([h - l, np.abs(h - pc), np.abs(l - pc)]), axis=0)
    str_, sp, sm = _wilder(tr, n), _wilder(pdm, n), _wilder(mdm, n)
    with np.errstate(invalid="ignore", divide="ignore"):
        pdi = 100 * sp / str_; mdi = 100 * sm / str_
        dx = 100 * np.abs(pdi - mdi) / (pdi + mdi)
    adx = np.full(len(c), np.nan)
    first = 2 * n - 1
    if len(c) > first:
        adx[first] = np.nanmean(dx[n:first + 1])
        for i in range(first + 1, len(c)):
            adx[i] = (adx[i - 1] * (n - 1) + dx[i]) / n
    return dx, adx, pdi, mdi


def _linreg(c, n=N):
    """slope and time-series forecast (value one bar ahead) of the last n closes."""
    x = np.arange(n, dtype=float); sx, sxx = x.sum(), (x * x).sum()
    slope = np.full(len(c), np.nan); tsf = np.full(len(c), np.nan)
    if len(c) < n:
        return slope, tsf
    w = np.lib.stride_tricks.sliding_window_view(c, n)
    sy = w.sum(1); sxy = (w * x).sum(1)
    m = (n * sxy - sx * sy) / (n * sxx - sx * sx)
    b = (sy - m * sx) / n
    slope[n - 1:] = m; tsf[n - 1:] = b + m * n
    return slope, tsf


def signals_series(d):
    h = np.asarray(d["high"], float); l = np.asarray(d["low"], float); c = np.asarray(d["close"], float)
    n = len(c)
    out = np.zeros(n, np.int8)
    if n < 3 * N:
        return out
    dx, adx, pdi, mdi = _dmi(h, l, c)
    slope, tsf = _linreg(c)
    tp = (h + l + c) / 3.0
    mid = np.full(n, np.nan); sd = np.full(n, np.nan)
    w = np.lib.stride_tricks.sliding_window_view(tp, 8)
    mid[7:] = w.mean(1); sd[7:] = w.std(1, ddof=1)
    bbu, bbl = mid + 2 * sd, mid - 2 * sd
    prev = lambda a: np.r_[np.nan, a[:-1]]
    with np.errstate(invalid="ignore"):
        s_up = (slope > 0) & (prev(slope) < slope)
        s_dn = (slope < 0) & (prev(slope) > slope)
        x_up = lambda a: (c > a) & (prev(c) <= prev(a))
        x_dn = lambda a: (c < a) & (prev(c) >= prev(a))
        long_ = s_up & (x_up(bbu) | x_up(tsf) | ((dx > mdi) & (adx > mdi) & (pdi > mdi)))
        short = s_dn & (x_dn(bbl) | x_dn(tsf) | ((dx > pdi) & (adx > pdi) & (mdi > pdi)))
    out[long_ & ~short] = 1
    out[short & ~long_] = -1
    return out
