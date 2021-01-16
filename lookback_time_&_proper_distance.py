"""
When astronomers observe a distant galaxy, they ask :
 - "How far away is that galaxy?"
 - "How long has the light from that galaxy been traveling?"

We can answer the first question by computing the proper distance dp(t0).
We can answer the second question by computing the lookback time.

"lookback time" = t0 - te
---------------
If light emitted at time te is observed at time t0, the lookback time is
simply t0 − te.

Both depend on the model universe.

Barbara Ryden: Introduction to cosmology, Cambridge, 2nd Ed. Page 147 (pdf)
"""

import numpy as np
import matplotlib.pyplot as plt
from astropy.cosmology import Planck13 as cosmo

z = np.linspace(0,10, 100)

# Lookback time
t_o_e = cosmo.lookback_time(z)

plt.scatter(z, t_o_e, s=1)
plt.xlabel('z')
plt.ylabel('t0-te (Gyr)')
plt.show()

# Proper distance
dp_t0 = cosmo.lookback_distance(z)
dp_te = dp_t0 / (1+z)

fig, ax = plt.subplots()
ax.scatter(z, dp_t0, s=1, label='At time of observation')
ax.scatter(z, dp_te, s=1, label='At time of emission')
plt.xlabel('z')
plt.ylabel('proper distance (Mpc)')
plt.legend()
plt.show()
