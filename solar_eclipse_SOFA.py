import erfa
import numpy as np
from scipy.signal import find_peaks
from datetime import datetime, timedelta


moonDiam = 3474.8 / 149597870.7
sunDiam = 1392680 / 149597870.7


def create_range(t1, t2, steps):
    rng = t2 - t1
    dt = rng / steps
    return [t1 + dt*i for i in range(steps+1)]

def get_tt(t):
    utc1, utc2 = erfa.dtf2d('UTC', t.year, t.month, t.day, t.hour, t.minute, t.second + (t.microsecond / 1e6))
    tai1, tai2 = erfa.utctai(utc1, utc2)
    tt1, tt2 = erfa.taitt(tai1, tai2)
    return tt1, tt2

def calc_distance(t, get_sizes=False):
    tt1, tt2 = get_tt(t)
    astrom, eo = erfa.apci13(tt1, tt2)
    sunGCRS = -astrom[2]*astrom[3]
    moonGCRS = erfa.moon98(tt1, tt2)[0]
    angDist = erfa.sepp(sunGCRS, moonGCRS) * erfa.DR2D
    if get_sizes:
        dSun = np.linalg.norm(sunGCRS)
        dMoon = np.linalg.norm(moonGCRS)
        thetaSun = 2 * np.arcsin(sunDiam / (2 * dSun)) * erfa.DR2D
        thetaMoon = 2 * np.arcsin(moonDiam / (2 * dMoon)) * erfa.DR2D
        return angDist, thetaSun, thetaMoon
    else:
        return angDist


def yearly_eclipse(year, threshold=1):
    t1 = datetime(year, 1, 1)
    t2 = datetime(year+1, 1, 1)
    rng = create_range(t1, t2, 365)
    d = np.array([calc_distance(i) for i in rng])
    peaks, _ = find_peaks(-d)
    monthlyTimes = [rng[i] for i in peaks]
    times = []
    dists = []
    for i, t in enumerate(monthlyTimes):
        rng = create_range(t-timedelta(hours=12), t+timedelta(hours=12), 1000)
        d = np.array([calc_distance(i) for i in rng])
        if np.min(d) < threshold:
            i_min = np.argmin(d)
            times.append(rng[i_min])
            dists.append(d[i_min])
    return times, dists


times, dists = yearly_eclipse(2024)

for i in range(len(times)):
    angDist, thetaSun, thetaMoon = calc_distance(times[i], get_sizes=True)
    print(times[i].isoformat()[:19].replace('T', ' '))
    print(f'Separation between centers   : {angDist:.3g}°')
    print(f'Angular diameter of the Sun  : {thetaSun:.3g}°')
    print(f'Angular diameter of the Moon : {thetaMoon:.3g}°')
    print('-'*50)


# Output:
"""
2024-04-08 18:17:59
Separation between centers   : 0.348°
Angular diameter of the Sun  : 0.533°
Angular diameter of the Moon : 0.553°
--------------------------------------------------
2024-10-02 18:45:15
Separation between centers   : 0.315°
Angular diameter of the Sun  : 0.533°
Angular diameter of the Moon : 0.49°
--------------------------------------------------
"""
