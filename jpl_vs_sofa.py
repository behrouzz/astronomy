import erfa
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from numeph import load_pickle


km2au = 6.684587122268446e-09
au2km = 149597870.7

def sofa2dt(date1, date2):
    yy, mm, dd, fd = erfa.jd2cal(date1, date2)
    h = int(fd * 24)
    res = (fd * 24) - h
    m = int(res * 60)
    res = (res * 60) - m
    s = int(res * 60)
    res = (res * 60) - s
    ms = int(res * 1e6)
    return datetime(yy, mm, dd, h, m, s, ms)


def get_tt(t):
    utc1, utc2 = erfa.dtf2d("UTC", t.year, t.month, t.day, t.hour,
                            t.minute, t.second + (t.microsecond / 1e6))
    tai1, tai2 = erfa.utctai(utc1, utc2)
    tt1, tt2 = erfa.taitt(tai1, tai2)
    return tt1, tt2

def jpl_barycentric_earth(tt):
    ssb_emb = dc[(0,3)].get_pos(tt)
    emb_ear = dc[(3,399)].get_pos(tt)
    ssb_ear_jpl = (ssb_emb + emb_ear) * km2au
    return ssb_ear_jpl


def sofa_barycentric_earth(tt1, tt2):
    pvh, pvb = erfa.epv00(tt1, tt2)
    return pvb[0]


def create_range(t1, t2, steps):
    rng = t2 - t1
    dt = rng / steps
    return [t1 + dt*i for i in range(steps+1)]

fname = 'C:/Moi/_py/Astronomy/Solar System/kernels/de440s.bsp'
dc = load_pickle('de440s_1900_2100.pickle')


t1 = datetime(2020, 1, 1)
t2 = datetime(2025, 1, 1)

rng = create_range(t1, t2, 100)[:-1]

#t = datetime.utcnow()

jpl = np.zeros((len(rng), 3))
sofa = np.zeros((len(rng), 3))
distance = []
for i, t in enumerate(rng):
    tt1, tt2 = get_tt(t)
    tt = sofa2dt(tt1, tt2)
    ssb_ear_jpl = jpl_barycentric_earth(tt)
    ssb_ear_sofa = sofa_barycentric_earth(tt1, tt2)
    dist_vec = ssb_ear_jpl - ssb_ear_sofa
    dist = np.linalg.norm(dist_vec) * au2km
    distance.append(dist)
    jpl[i] = ssb_ear_jpl
    sofa[i] = ssb_ear_sofa


plt.plot(rng, distance)
#plt.plot(rng, (jpl[:,2]-sofa[:,2]))
plt.grid()
plt.show()
