# IAU 2006 precession / 2000A nutation model

import erfa
import numpy as np
import matplotlib.pyplot as plt

jd2000 = 2451545

t1 = jd2000 - (13000 * 365.25)
t2 = jd2000 + (13000 * 365.25)

rng = np.arange(t1, t2, 365250)

ra = np.zeros((len(rng),))
dec = np.zeros((len(rng),))

for i, tt in enumerate(rng):
    r = erfa.pnm06a(tt, 0)
    ra[i], dec[i] = erfa.c2s(r[-1, :])

#ra = erfa.anp(ra)

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.scatter(ra, 90-(dec*erfa.DR2D), s=2)

ax.set_theta_direction(-1)
ax.set_theta_offset(np.pi/2.0)

for i in range(len(rng)):
    ax.text(ra[i], 90-(dec[i]*erfa.DR2D),
            s=str(int((rng[i] - jd2000)/365.25)),
            fontsize='small', alpha=0.5)

plt.title('GCRS Position of CIP, years since J2000')
plt.show()

