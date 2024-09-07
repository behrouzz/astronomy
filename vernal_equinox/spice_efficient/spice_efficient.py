import erfa
import numpy as np
import spiceypy as sp
import matplotlib.pyplot as plt

def true_sun(et):
    rotmat = sp.sxform('J2000', 'TETE', et)[:3,:3]
    pos, _ = sp.spkez(10, et, 'J2000', 'LT+S', 399)
    sunJ2000 = pos[:3] #GCRS
    sun = np.matmul(rotmat, sunJ2000)
    ra, dec = erfa.c2s(sun)
    return dec

sp.furnsh('k_1600_2600.tm')

year_length = 365.25*86400
y0 = 6809764.971984705 #2000

times = []

N = 100

#start
for gooz in range(N):
    y1 = y0 + year_length


    et_i = y1 - (86400*5)
    et_f = y1 + (86400*5)

    # start
    while (et_f - et_i) > 1e-6:
        rng = np.linspace(et_i, et_f, 3)

        dec = np.zeros((2,))
        for i, et in enumerate([rng[:2].mean(), rng[1:].mean()]):
            dec[i] = true_sun(et)
        if abs(dec[0]) < abs(dec[1]):
            et_f = (et_i + et_f) / 2
        else:
            et_i = (et_i + et_f) / 2

    y1 = et_i
    times.append(y1)
    year_length = y1 - y0
    y0 = y1

sp.kclear()

times = np.array(times)
dt = (times[1:] - times[:-1]) / 86400
print(dt)

plt.scatter(range(N-1), dt-365)
plt.plot(range(N-1), dt-365)
plt.show()
