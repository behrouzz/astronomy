import numpy as np
from datetime import datetime, timedelta
import spiceypy as sp
from hypatie import mag
import matplotlib.pyplot as plt

names = ['sun', 'mercury', 'venus', 'moon', 'mars',
         'jupiter', 'saturn', 'uranus', 'neptune', 'pluto']

G = 6.6743e-11 #m3/(kg s2)
M_sun = 1.988409870698051e+30 # kg
M_earth = 5.972167867791379e+24
M_moon = 7.348e+22
M_mercury = 3.301e+23
M_venus = 4.867e+24
M_mars = 6.416999999999999e+23
M_jupiter = 1.8981245973360505e+27
M_saturn = 5.685e+26
M_uranus = 8.682000000000001e+25
M_neptune = 1.0240000000000001e+26
M_pluto = 1.30900e+22


def force(pos, m):
    r = pos * 1000 # km to m
    unit = r / mag(r)
    f = (-G * (M_earth*m) * unit) / (mag(r)**2)
    return f


sp.furnsh('data/naif0012.tls')
sp.furnsh('data/de440s.bsp')


def get_forces(t):
    et = sp.str2et(str(t))
        
    sun = sp.spkez(10, et, 'J2000', 'LT', 399)[0][:3]
    mer = sp.spkez(1, et, 'J2000', 'LT', 399)[0][:3]
    ven = sp.spkez(2, et, 'J2000', 'LT', 399)[0][:3]
    moo = sp.spkez(301, et, 'J2000', 'LT', 399)[0][:3]
    mar = sp.spkez(4, et, 'J2000', 'LT', 399)[0][:3]
    jup = sp.spkez(5, et, 'J2000', 'LT', 399)[0][:3]
    sat = sp.spkez(6, et, 'J2000', 'LT', 399)[0][:3]
    ura = sp.spkez(7, et, 'J2000', 'LT', 399)[0][:3]
    nep = sp.spkez(8, et, 'J2000', 'LT', 399)[0][:3]
    plu = sp.spkez(9, et, 'J2000', 'LT', 399)[0][:3]


    f_sun = force(sun, M_sun)
    f_mer = force(mer, M_mercury)
    f_ven = force(ven, M_venus)
    f_moo = force(moo, M_moon)
    f_mar = force(mar, M_mars)
    f_jup = force(jup, M_jupiter)
    f_sat = force(sat, M_saturn)
    f_ura = force(ura, M_uranus)
    f_nep = force(nep, M_neptune)
    f_plu = force(plu, M_pluto)

    
    forces = [f_sun, f_mer, f_ven, f_moo, f_mar, f_jup, f_sat, f_ura, f_nep, f_plu]
    dc = {k:v for (k,v) in zip(names, forces)}
    return dc


t0 = datetime(2000, 1, 1)

t_win = [t0 + timedelta(days=i) for i in range(1000)]

f = []
for t in t_win:
    dc = get_forces(t)
    f.append(mag(sum(dc.values())))

plt.scatter(t_win, f, s=1)
plt.show()

sp.kclear()
