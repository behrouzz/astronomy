"""
Current proper distance as a function of z
==========================================
Here, we use three methods to calculate current proper distance (dp0) from z.

1) The first method is using this formula:

   cz = H0d
   => dp0 = c*z / H0

   This does not wok for large redshifts.

2) The second method is using a formula that has been extracted from a Taylor
   expansion approximation for scale factor.

   dp0 = (z*c/H0) * (1-(z*(1+q0)/2))

3) The third method is using astropy's '.lookback_distance()' method.
"""

from astropy.cosmology import Planck13 as cosmo
from astropy.constants import G, c
import numpy as np
import matplotlib.pyplot as plt



Or0 = cosmo.Ogamma(0) + cosmo.Onu(0)
Om0 = cosmo.Om(0)
Ode0 = cosmo.Ode(0)

# deceleration parameter (equation 6.11)
q0 = Or0 + 0.5*Om0 - Ode0 

H0 = cosmo.H(0).to('1 / s')

z = np.linspace(0, 2, 100)

# current proper distance in terms of z (equation 6.12)
dp0_612 = c*z / H0
dp0_612 = dp0_612.to('Mpc')

# current proper distance in terms of z (equation 6.19)
dp0_619 = (z*c/H0) * (1-(z*(1+q0)/2))
dp0_619 = dp0_619.to('Mpc')


# current proper distance in terms of z (equation 6.19)

fig, ax = plt.subplots()
ax.scatter(z, dp0_612, s=1, label='d=cz/H0')
ax.scatter(z, dp0_619, s=1, label='equation 6.19')
ax.scatter(z, cosmo.lookback_distance(z), s=1, label='astropy')
plt.legend()
plt.xlabel('z')
plt.ylabel('Current proper distance (Mpc)')
plt.show()
