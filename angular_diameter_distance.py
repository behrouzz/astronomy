# page 168 pdf
"""
Critical redshift
=================
In each cosmological model (other than lambda-only model), there is a
critical redshift (cz) at which the angular size is minimum. It means
that from z=0 to z=zc the angular size decreases, but with redshifts
more than zc, the angular size will increase (i.e. the angular diameter
distance (dA) will decrease.

So, there's a maximum for the angular diameter distance (dA_max), which
is the angular diameter distance at zc.

Here, we will calculate dA_max and zc for the standard model and then
we will show the relation between dA and z in a diagram.
"""

import numpy as np
from astropy.cosmology import Planck13 as cosmo
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

z = np.linspace(0, 5, 10000)

dA = cosmo.angular_diameter_distance(z)

print('Maximum angular diameter distance :', dA.max())
c_ind = np.argmax(dA.value)
print('Critical redshift : ', z[c_ind])

fig, ax = plt.subplots()
ax.scatter(z, dA, s=1)
plt.xlabel('z')
plt.ylabel('Angular diameter distance (Mpc)')
plt.show()

