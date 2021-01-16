"""
Calculating Scale Factor
========================

# Benchmark Model is Flat and consists of: Radiation, Matter and Lambda
# So: omega_R0 + omega_M0 + omega_LAMBDA0 = 1
# Knowing these parameters, we can use Friedmann eq 5.81 , 5.83

# Radiation in Benchmark Model consists of photons and neutrinos
# Photons are assumed to be provided solely by CMB

Page 144 pdf
"""

import numpy as np
import scipy.integrate as integrate
import matplotlib.pyplot as plt
from astropy import units as u
import seaborn as sns
sns.set()


# Known parameters of the Benchmark Model
# ---------------------------------------
H0 = 68 * u.Unit("km / (Mpc s)")

# Radiation
Oph0 = 5.35 * 10**-5 # Photons (CMB)
One0 = 3.65 * 10**-5 # Neutrinos
Or0 = Oph0 + One0

# Matter
Oba0 = 0.048 # Baryonic matter
Odm0 = 0.262 # Nonbaryonic dark matter
Om0 = Oba0 + Odm0

# Cosmological constant
Ode0 = 0.69 # Lambda (dark energy)

# All components
Oall = Or0 + Om0 + Ode0

#==========================================


a = np.linspace(0.0001, 3, 10000)
func = lambda a: 1 / np.sqrt( Or0/a**2 + Om0/a + Ode0*a**2 + 1-Oall)
t = [(integrate.quad(func, 0, i)[0]/H0).to('Gyr').value for i in a]

plt.scatter(t, a, s=1)
plt.xlabel('Billion years from Big Bang')
plt.ylabel('Scale factor')
plt.show()
