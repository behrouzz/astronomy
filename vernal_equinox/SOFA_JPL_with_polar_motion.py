import erfa
from datetime import datetime, timedelta
import numpy as np
import spiceypy as sp
from iers import EOP
#pos_gcrs = pos_icrs - earth_icrs

KM2AU = 1 / 149597870.7
KMpS2AUpD = 0.0005775483273639937

#BASE = 'C:/Moi/_py/Astronomy/Solar System/kernels/'
BASE = 'C:/Users/H21/Desktop/Desktop/Behrouz/Astronomy/kernels/'

kernels = ['naif0012.tls', 'pck00010.tpc', 'de440s.bsp'] #'earth_latest_high_prec.bpc'
kernels = [BASE + i for i in kernels]



def create_range(t1, t2, steps):
    rng = t2 - t1
    dt = rng / steps
    return [t1 + dt*i for i in range(steps+1)]

def get_time(t):
    utc1, utc2 = erfa.dtf2d('UTC', t.year, t.month, t.day, t.hour, t.minute, t.second + (t.microsecond / 1e6))
    tai1, tai2 = erfa.utctai(utc1, utc2)
    tt1, tt2 = erfa.taitt(tai1, tai2)
    return utc1, utc2, tt1, tt2


def get_earth(t, kernels): #not used in this file
    """
    Heliocentric and Barycentric position-velocity of Earth
    """
    et = sp.str2et(str(t))
    
    state, lt = sp.spkez(targ=10, et=et, ref='J2000', abcorr='NONE', obs=0)
    pb_sun, vb_sun, lt_sun = state[:3], state[3:], lt

    state, lt = sp.spkez(targ=399, et=et, ref='J2000', abcorr='NONE', obs=10)
    ph_ear, vh_ear, lth_ear = state[:3]*KM2AU, state[3:]*KMpS2AUpD, lt

    state, lt = sp.spkez(targ=399, et=et, ref='J2000', abcorr='NONE', obs=0)
    pb_ear, vb_ear, ltb_ear = state[:3]*KM2AU, state[3:]*KMpS2AUpD, lt

    # Return results adapted to SOFA epv00 format
    pvh = np.array([ph_ear, vh_ear])
    pvb = np.array([pb_ear, vb_ear])

    return pvh, pvb

def get_sun_gcrs(t, kernels):
    et = sp.str2et(str(t))
    state, lt = sp.spkez(targ=10, et=et, ref='J2000', abcorr='NONE', obs=399)
    p_sun_gcrs, v_sun_gcrs, lt_sun_gcrs = state[:3], state[3:], lt
    p_sun_gcrs *= KM2AU
    v_sun_gcrs *= KMpS2AUpD
    return p_sun_gcrs, v_sun_gcrs, lt_sun_gcrs


def gcrs_to_true_equator(utc1, utc2, tt1, tt2, pos_gcrs, eop):
    dc = eop.get_eop(utc1 + utc2)
    xp = dc['px'] * erfa.DAS2R
    yp = dc['py'] * erfa.DAS2R
    dx = dc['dx'] * erfa.DMAS2R
    dy = dc['dy'] * erfa.DMAS2R
    
    x, y = erfa.xy06(tt1, tt2)
    x += dx
    y += dy
    s = erfa.s06(tt1, tt2, x, y)
    bpn = erfa.c2ixys(x, y, s) #givec CIRS
    # Apply polar motion
    pom = erfa.ir()
    pom = erfa.ry(-xp, pom)
    pom = erfa.rx(-yp, pom)
    r = erfa.rxr(pom, bpn)
    pos_true_equator = erfa.rxp(r, pos_gcrs)
    return pos_true_equator


year = 2024
t1 = datetime(year, 3, 19)
t2 = datetime(year, 3, 21)
rng = create_range(t1, t2, 1000)

eop = EOP()

for k in kernels:
    sp.furnsh(k)

dec = np.zeros((len(rng),))
lt = np.zeros((len(rng),))

for i, t in enumerate(rng):
    utc1, utc2, tt1, tt2 = get_time(t)
    p_sun_gcrs, _, lt[i] = get_sun_gcrs(t, kernels)
    p_sun_true = gcrs_to_true_equator(utc1, utc2, tt1, tt2, p_sun_gcrs, eop)
    _, dec[i], _ = erfa.p2s(p_sun_true)

 

sp.kclear()

x = dec
y = np.array([i.timestamp() for i in rng])
t_ = np.interp(0, x, y)
t = datetime.fromtimestamp(t_)


t_lt = np.interp(t_, y, lt)
t = t + timedelta(seconds=t_lt)

print('UTC   :', t)
print('Tehran:', t + timedelta(hours=3.5))


