# page 156 pdf
import numpy as np
from astropy.cosmology import Planck13 as cosmo
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

Or0 = cosmo.Ogamma(0) + cosmo.Onu(0)
Om0 = cosmo.Om(0)
Ode0 = cosmo.Ode(0)

H0 = cosmo.H(0)
t0 = cosmo.age(0)
q0 = Or0 + 0.5*Om0 - Ode0 #equation 6.11

t = np.linspace(0, t0, 1000)

a = 1 + H0*(t-t0) - 0.5*q0*(H0**2)*(t-t0)**2

fig, ax = plt.subplots()
ax.scatter(t, a, s=1)
plt.show()

