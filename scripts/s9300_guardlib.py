# s9300_guardlib.py - helper for the GUARD paper scripts (22 Nov 2026). Not a script (name ends in "lib").
# A guard = a script that wins on crazy days (hard-days test). Rule found in EARLY_CRAZY_v2 (both years positive, small):
# trade it ONLY in the first 2 hours after its market's session open, and ONLY when the last 5 days moved more than
# normal ("crazy week": mean daily range of the last 5 days >= 1.3 x the mean of the last 20 days; known before the open).
import os, re, glob, importlib.util, datetime as dt
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_CACHE = {}


def load_original(name):
    """Find the original script in this folder by its NAME = "..." line (None if not found)."""
    if name in _CACHE:
        return _CACHE[name]
    mod = None
    pat = re.compile(r'^NAME\s*=\s*["\']' + re.escape(name) + r'["\']', re.M)
    for p in sorted(glob.glob(os.path.join(_HERE, "*.py"))):
        b = os.path.basename(p)
        if b.startswith("s93") or b.endswith("lib.py"):
            continue
        try:
            txt = open(p, encoding="utf-8", errors="ignore").read()
        except Exception:
            continue
        if pat.search(txt):
            try:
                spec = importlib.util.spec_from_file_location("guard_orig_" + re.sub(r"\W", "_", name), p)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
            except Exception:
                mod = None
            break
    _CACHE[name] = mod
    return mod


def _nth_sunday(y, m, n):
    d = dt.date(y, m, 1); d += dt.timedelta(days=(6 - d.weekday()) % 7)
    return d + dt.timedelta(days=7 * (n - 1))


def _last_sunday(y, m):
    d = (dt.date(y, m + 1, 1) - dt.timedelta(days=1)) if m < 12 else dt.date(y, 12, 31)
    return d - dt.timedelta(days=(d.weekday() + 1) % 7)


def session_open_utc(day, sym):
    """UTC seconds of the session open on calendar date `day` for this asset."""
    s = sym.upper(); y = day.year
    if s.startswith(("USTEC", "US30", "US500")):
        dst = _nth_sunday(y, 3, 2) <= day < _nth_sunday(y, 11, 1); hh, mm, off = 9, 30, (-4 if dst else -5)
    elif s.startswith(("DE30", "STOXX50")):
        dst = _last_sunday(y, 3) <= day < _last_sunday(y, 10); hh, mm, off = 9, 0, (2 if dst else 1)
    elif s.startswith("JP225"):
        hh, mm, off = 9, 0, 9
    elif s.startswith("HK50"):
        hh, mm, off = 9, 30, 8
    else:                                                   # UK100, gold, silver, oil, FX, BTC: London 08:00
        dst = _last_sunday(y, 3) <= day < _last_sunday(y, 10); hh, mm, off = 8, 0, (1 if dst else 0)
    return int(dt.datetime(y, day.month, day.day, hh, mm, tzinfo=dt.timezone.utc).timestamp()) - off * 3600


def guard_mask(d, window_min=120, ratio=1.3):
    """True on candles inside the first `window_min` minutes after the session open, on 'crazy week' days only."""
    t = np.asarray(d["time"], dtype=np.int64); h = np.asarray(d["high"]); l = np.asarray(d["low"])
    sym = str(d.get("symbol", ""))
    n = len(t); out = np.zeros(n, bool)
    if n == 0:
        return out
    day = t // 86400
    uniq, start = np.unique(day, return_index=True)
    end = np.r_[start[1:], n]
    rng = np.array([h[a:b].max() - l[a:b].min() for a, b in zip(start, end)])
    for k, dd in enumerate(uniq):
        if k < 10:
            continue
        last5 = rng[max(0, k - 5):k].mean(); last20 = rng[max(0, k - 20):k].mean()
        if not (last20 > 0 and last5 / last20 >= ratio):
            continue
        date = dt.datetime.fromtimestamp(int(dd) * 86400, dt.timezone.utc).date()
        if date.weekday() >= 5:
            continue
        op = session_open_utc(date, sym)
        a, b = start[k], end[k]
        out[a:b] = (t[a:b] >= op) & (t[a:b] < op + window_min * 60)
    return out
