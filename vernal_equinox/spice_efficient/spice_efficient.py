import erfa
import numpy as np
import spiceypy as sp
import pandas as pd


J2000 = 2451545

def et2tt(et):
    tt = J2000 + (et / 86400)
    return tt

def tt2et(tt):
    et = (tt - J2000) * 86400
    return et

def true_sun(et):
    rotmat = sp.sxform('J2000', 'TETE', et)[:3,:3]
    pos, _ = sp.spkez(10, et, 'J2000', 'LT+S', 399)
    sunJ2000 = pos[:3] #GCRS
    sun = np.matmul(rotmat, sunJ2000)
    ra, dec = erfa.c2s(sun)
    return dec

def do_loop(et_guess):
    et_i = et_guess - (86400*5)
    et_f = et_guess + (86400*5)
    while (et_f - et_i) > 1e-3:
        rng = np.linspace(et_i, et_f, 3)
        dec = np.zeros((2,))
        for i, et in enumerate([rng[:2].mean(), rng[1:].mean()]):
            dec[i] = true_sun(et)
        if abs(dec[0]) < abs(dec[1]):
            et_f = (et_i + et_f) / 2
        else:
            et_i = (et_i + et_f) / 2
    et = np.interp(0, dec, np.array([rng[:2].mean(), rng[1:].mean()]))
    return et


def go(n, back=False):
    y0 = 6809764.971984705 #2000
    year_length = 365.25*86400
    if back:
        year_length *= -1
    times = np.zeros((n,))
    for i in range(n):
        y1 = do_loop(y0 + year_length)
        times[i] = y1
        year_length = y1 - y0
        y0 = y1
    return times



sp.furnsh('k_1600_2600.tm')
N = 100
times = go(N)#, back=True)
sp.kclear()

df = pd.DataFrame({'et':times})
df['tt'] = J2000 + (df['et'].values / 86400) #not exactly!
df['persian'] = np.arange(len(df)) + 1380 #=2001 (if back use '-')
df['gregorian'] = df['persian'] + 621

df['diff'] = df['et'].diff() - (365*86400)

"""
Note: TT is not exact since ET is actually TDB
"""
