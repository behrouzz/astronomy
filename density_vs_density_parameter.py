"""
Density vs Density Parameter
============================
Our universe is composed of different components, such as matter, dark-matter,
dark-energy, etc. We can show the density of each of these components in
different ways.

Energy Density
--------------
Since in the general relativistic point of view, matter and energy are the
same phenomen (E=MC2), we can consider the density of each component as its
energy density.

Critical Energy Density (ced)
-----------------------------
Considering the energy density of all of the components of the universe, we
can define a critical energy density (ced) at any moment of the cosmic time
as:

ced = ((3 * c**2) / (8 * np.pi * G)) * H**2

Where:
c is the speed of light
G is the gravitational constant
H is the Hubble parameter at time t

If the total energy density at t is more than this value (ced) at t, the
curvature of the universe is positive at t; if the total energy density at t
is less than this value (ced), the curvature of the universe is negative.

Density Parameter (Omega)
-------------------------
If the divide the energy density of each component by the rritical energy
density, we find its density parameter (Omega). So, each component of the
universe has an omega at time t which is dimensionless.

In this script, I have choosed three components (matter, dark-matter,
dark-energy) and I will show you two plots:

1) Density Parameter (Omega) of each component vs Time
2) Energy Density of each component vs Time

Since the energy density of matter and dark-matter is extremely huge in the
begining of the cosmic time, I have ignored the first 3 Gyrs period from the
Big Bang in the second plot.

You can see in the second plot that the energy density of the dark energy is
constant with time. Since the universe is expanding, it means that with
expansion, new dark energy is created. This is why we think that it should
be 'vacuum energy'.

Behrouz Safari
Strasbourg, 14 jan 2021
https://github.com/behrouzz/
"""

import numpy as np
from astropy.cosmology import Planck13 as cosmo
from astropy.constants import c, G
from astropy.cosmology import z_at_value
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

t0 = cosmo.age(0)
time_window = np.linspace(0, t0, 100)[1:-1]
z = [z_at_value(cosmo.age, t) for t in time_window]

H = cosmo.H(z)

# critical energy density of universe (all components)
ced = ((3 * c**2) / (8 * np.pi * G)) * H**2

# Plotting Omega (density parameter)
fig, ax = plt.subplots()
ax.scatter(time_window, cosmo.Om(z), s=1, c='b', label='Matter')
ax.scatter(time_window, cosmo.Odm(z), s=1, c='k', label='Dark Matter')
ax.scatter(time_window, cosmo.Ode(z), s=1, c='brown', label='Dark Energy')
plt.xlabel('Time (age of universe in Gyr)')
plt.ylabel('Density Parameter (Omega)')
ax.legend()
plt.show()

# Plotting energy density (ignoring the first 3 Gyrs from Big Bang)
matter = (cosmo.Om(z) * ced).to('MeV / m3')
dark_matter = (cosmo.Odm(z) * ced).to('MeV / m3')
dark_energy = (cosmo.Ode(z) * ced).to('MeV / m3')

fig, ax = plt.subplots()
ax.scatter(time_window[20:], matter[20:], s=1, c='b', label='Matter')
ax.scatter(time_window[20:], dark_matter[20:], s=1, c='k', label='Dark Matter')
ax.scatter(time_window[20:], dark_energy[20:], s=1, c='brown', label='Dark Energy')
plt.xlabel('Time (age of universe in Gyr)')
plt.ylabel('Density (in MeV / m3)')
ax.legend()
plt.show()
