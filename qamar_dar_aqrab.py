import numpy as np
import spiceypy as sp
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from hypatie import sph2car, car2sph
from hypatie.transform import angular_separation
from scipy.signal import find_peaks


# Antares
ra, dec = 247.3519154198264, -26.432002611950832
r = 5203401759919440 #km
ant_icrs_sph = np.array([ra, dec, r])
ant_icrs = sph2car(ant_icrs_sph)

t1 = datetime(2023, 1, 1)
t2 = datetime(2024, 1, 1)
steps = 50000
rng = t2 - t1
dt = rng / steps
ts = np.array([t1 + dt*i for i in range(steps+1)])


adr = 'C:/Moi/_py/Astronomy/Solar System/kernels/'

kernels = [
    adr + 'naif0012.tls',
    adr + 'pck00010.tpc',
    adr + 'de440s.bsp',
    ]

for k in kernels:
    sp.furnsh(k)


ets = [sp.str2et(str(t)) for t in ts]
pos = np.zeros((len(ets),3))
for i, et in enumerate(ets):
    state, lt = sp.spkez(targ=301, et=et, ref='J2000', abcorr='LT+S', obs=399)
    pos[i,:] = state[:3]


sp.kclear()

moon_sph = car2sph(pos)
m_ra = moon_sph[:, 0]
m_dec = moon_sph[:, 1]


d = [angular_separation(ra, dec, m_ra[i], m_dec[i]) for i in range(len(ts))]
d = np.array(d)
new_d = 100 - np.where(d>0, d, np.nan)

peaks, _ = find_peaks(new_d, distance=10)

for i in peaks:
    print(ts[i], ':', d[i])

fig, ax = plt.subplots()
ax.scatter(ts[peaks], new_d[peaks], s=10, c='r')
ax.scatter(ts, new_d, s=1, c='b', alpha=0.5)
plt.grid()
plt.show()

