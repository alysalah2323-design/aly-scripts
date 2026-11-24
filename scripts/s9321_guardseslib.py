# s9321_guardseslib.py - helper for the SESSION GUARDS (24 Nov 2026). Not a script (name ends in "lib").
# From NIGHT_PROTECT4: these script+asset won in ONE Cairo session on "crazy week" days in BOTH years, with almost all
# the signs tested (not just one) -> paper guards: trade only in that Cairo session, only in a crazy week
# (mean daily range of the last 5 days >= 1.3 x the last 20 days, known before the day starts).
import numpy as np
import salylib as L
import s9300_guardlib as G


def crazy_week_session(d, cairo_from, cairo_to, ratio=1.3):
    t = np.asarray(d["time"], dtype=np.int64); h = np.asarray(d["high"]); l = np.asarray(d["low"])
    n = len(t); out = np.zeros(n, bool)
    if n == 0:
        return out
    day = t // 86400
    uniq, start = np.unique(day, return_index=True)
    end = np.r_[start[1:], n]
    rng = np.array([h[a:b].max() - l[a:b].min() for a, b in zip(start, end)])
    mod, _ = L.cairo_minutes(t)
    hr = mod // 60
    insess = (hr >= cairo_from) & (hr < cairo_to)
    for k in range(10, len(uniq)):
        last5 = rng[max(0, k - 5):k].mean(); last20 = rng[max(0, k - 20):k].mean()
        if last20 > 0 and last5 / last20 >= ratio:
            a, b = start[k], end[k]
            out[a:b] = insess[a:b]
    return out


def make(orig_name, asset, cairo_from, cairo_to):
    o = G.load_original(orig_name)

    def signals_series(d):
        n = len(d["close"])
        if o is None or not str(d.get("symbol", "")).upper().startswith(asset):
            return np.zeros(n, np.int8)
        s = np.nan_to_num(np.asarray(o.signals_series(d), float)).astype(np.int8)
        return np.where(crazy_week_session(d, cairo_from, cairo_to), s, 0).astype(np.int8)

    sl = (lambda d: o.sl_series(d)) if (o is not None and hasattr(o, "sl_series")) else None
    return o, signals_series, sl
