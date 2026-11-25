# s9330_newslib.py - helper for the NEWS GUARDS on paper (25 Nov 2026). Not a script (name ends in "lib").
# 10 script+asset won at US high-impact news (CPI / NFP / FOMC) in BOTH backtest years, but a luck test (same hours on
# days without news) could not prove it -> paper only: they trade ONLY from 15 min before to 60 min after the release.
import datetime as dt
import numpy as np
import s9300_guardlib as G

CPI = ["2026-12-10", "2027-01-13", "2027-02-11", "2027-03-10", "2027-04-13", "2027-05-12", "2027-06-10", "2027-07-14",
       "2027-08-11", "2027-09-14", "2027-10-14", "2027-11-10", "2027-12-10"]
NFP = ["2026-12-04", "2027-01-08", "2027-02-05", "2027-03-05", "2027-04-02", "2027-05-07", "2027-06-04", "2027-07-02",
       "2027-08-06", "2027-09-03", "2027-10-08", "2027-11-05", "2027-12-03"]
FOMC = ["2026-12-09", "2027-01-27", "2027-03-17", "2027-04-28", "2027-06-09", "2027-07-28", "2027-09-15", "2027-11-17"]
BEFORE_MIN, AFTER_MIN = 15, 60


def _ny_offset(day):
    y = day.year
    st = dt.date(y, 3, 1); st += dt.timedelta(days=(6 - st.weekday()) % 7 + 7)      # 2nd Sunday of March
    en = dt.date(y, 11, 1); en += dt.timedelta(days=(6 - en.weekday()) % 7)         # 1st Sunday of November
    return -4 if st <= day < en else -5


def news_utc():
    out = []
    for days, hh, mm in ((CPI, 8, 30), (NFP, 8, 30), (FOMC, 14, 0)):
        for s in days:
            d = dt.date.fromisoformat(s)
            loc = dt.datetime(d.year, d.month, d.day, hh, mm, tzinfo=dt.timezone.utc)
            out.append(int((loc - dt.timedelta(hours=_ny_offset(d))).timestamp()))
    return np.array(sorted(out), dtype=np.int64)


NEWS = news_utc()


def in_news_window(close_ts, news=None):
    """True where the bar CLOSE time is between 15 min before and 60 min after a release."""
    nt = NEWS if news is None else news
    t = np.asarray(close_ts, dtype=np.int64)
    i = np.searchsorted(nt, t, side="right")
    prev = np.where(i > 0, nt[np.maximum(i - 1, 0)], -10 ** 12)
    nxt = np.where(i < len(nt), nt[np.minimum(i, len(nt) - 1)], 10 ** 12)
    return ((t - prev) <= AFTER_MIN * 60) | ((nxt - t) <= BEFORE_MIN * 60)


def make(orig_name, asset):
    o = G.load_original(orig_name)

    def signals_series(d):
        n = len(d["close"])
        if o is None or not str(d.get("symbol", "")).upper().startswith(asset):
            return np.zeros(n, np.int8)
        s = np.nan_to_num(np.asarray(o.signals_series(d), float)).astype(np.int8)
        t = np.asarray(d["time"], dtype=np.int64)
        step = int(np.median(np.diff(t))) if n > 1 else 900
        return np.where(in_news_window(t + step), s, 0).astype(np.int8)

    sl = (lambda d: o.sl_series(d)) if (o is not None and hasattr(o, "sl_series")) else None
    return o, signals_series, sl
