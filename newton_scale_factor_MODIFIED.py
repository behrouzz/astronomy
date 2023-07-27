import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import spiceypy as sp
from astropy.constants import G, M_sun, M_earth, au, c
import astropy.units as u

M_moon = 7.348e+22 * u.kg
M_mercury = 3.301e+23 * u.kg
M_venus = 4.867e+24 * u.kg
M_mars = 6.416999999999999e+23 * u.kg
M_jupiter = 1.8981245973360505e+27 * u.kg
M_saturn = 5.685e+26 * u.kg
M_uranus = 8.682000000000001e+25 * u.kg
M_neptune = 1.0240000000000001e+26 * u.kg
M_pluto = 1.30900e+22 * u.kg

def mag(x):
    return np.linalg.norm(np.array(x))

def unit(x):
    return x / mag(x)


def get_state(targ, t):
    ts = [t, t+timedelta(microseconds=1)]
    pos = []
    vel = []
    for t in ts:
        et = sp.str2et(str(t))
        state, _ = sp.spkez(targ=targ, et=et, ref='J2000', abcorr='NONE', obs=0)
        pos.append(state[:3])
        vel.append(state[3:])
    a = (vel[1] - vel[0]) / (1e-06)
    return pos[0]*u.Unit('km'), vel[0]*u.Unit('km/s'), a*u.Unit('km/s2')


def get_F(targ, m, t):
    p, v, a = get_state(targ, t)
    F = (m * a).to('N')
    return F


def force_on_earth(targ, t, m):
    et = sp.str2et(str(t))
    state, _ = sp.spkez(targ=targ, et=et, ref='J2000', abcorr='LT', obs=399)
    p = state[:3]
    d = mag(p) * u.km
    f = (-G*m*M_earth)/(d**2)
    F = f * unit(p)
    return F.to('N')

def force_on_earth_with_gamma(targ, t, m):
    et = sp.str2et(str(t))
    state, _ = sp.spkez(targ=targ, et=et, ref='J2000', abcorr='LT', obs=399)
    p = state[:3]
    v = state[3:] * u.Unit('km/s')
    speed = mag(v.value) * v.unit
    gamma = (1 - ((speed**2)/c**2)) ** 0.5
    d = mag(p) * u.km
    f = (-G*m*M_earth*gamma)/(d**2)
    F = f * unit(p)
    return F.to('N')
    
adr = 'C:/Moi/_py/Astronomy/Solar System/kernels/'
kernels = [adr+'de440s.bsp', adr+'naif0012.tls']

for k in kernels:
    sp.furnsh(k)

#===============================================================

t = datetime(2023, 1, 1)

# total Force on Earth
F = get_F(targ=399, m=M_earth, t=t)


# sum of each of forces on Earth (Newton's formula)
f_sun = force_on_earth(10, t, M_sun)
f_moo = force_on_earth(301, t, M_moon)
f_mer = force_on_earth(1, t, M_mercury)
f_ven = force_on_earth(2, t, M_venus)
f_mar = force_on_earth(4, t, M_mars)
f_jup = force_on_earth(5, t, M_jupiter)
f_sat = force_on_earth(6, t, M_saturn)
f_ura = force_on_earth(7, t, M_uranus)
f_nep = force_on_earth(8, t, M_neptune)
f_plu = force_on_earth(9, t, M_pluto)

f_sum = f_sun + f_moo + f_mer + f_ven + f_mar +\
        f_jup + f_sat + f_ura + f_nep + f_plu

print(mag(f_sum)/mag(F))

# sum of each of forces on Earth (with gamma)
f_sun = force_on_earth_with_gamma(10, t, M_sun)
f_moo = force_on_earth_with_gamma(301, t, M_moon)
f_mer = force_on_earth_with_gamma(1, t, M_mercury)
f_ven = force_on_earth_with_gamma(2, t, M_venus)
f_mar = force_on_earth_with_gamma(4, t, M_mars)
f_jup = force_on_earth_with_gamma(5, t, M_jupiter)
f_sat = force_on_earth_with_gamma(6, t, M_saturn)
f_ura = force_on_earth_with_gamma(7, t, M_uranus)
f_nep = force_on_earth_with_gamma(8, t, M_neptune)
f_plu = force_on_earth_with_gamma(9, t, M_pluto)

f_sum = f_sun + f_moo + f_mer + f_ven + f_mar +\
        f_jup + f_sat + f_ura + f_nep + f_plu

print(mag(f_sum)/mag(F))

#===============================================================
sp.kclear()
