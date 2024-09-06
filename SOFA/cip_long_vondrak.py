# Vondrak et al. (2011, 2012) 400 millennia precession model + Bias

import erfa
import numpy as np
import matplotlib.pyplot as plt

ep1 = 2000 - 13000
ep2 = 2000 + 13000

rng = np.arange(ep1, ep2, 1000)

ra = np.zeros((len(rng),))
dec = np.zeros((len(rng),))

for i, epj in enumerate(rng):
    r = erfa.ltpb(epj)
    ra[i], dec[i] = erfa.c2s(r[-1, :])

#ra = erfa.anp(ra)

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.scatter(ra, 90-(dec*erfa.DR2D), s=3)

ax.set_theta_direction(-1)
ax.set_theta_offset(np.pi/2.0)

for i in range(len(rng)):
    ax.text(ra[i], 90-(dec[i]*erfa.DR2D),
            s=str(int((rng[i]))),
            fontsize='small', alpha=0.5)

plt.title('GCRS Position of CIP (Julian Epoch)')
plt.show()

