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

a = np.linspace(0.0001, 5, 100)
func = lambda a: 1 / np.sqrt( Or0/a**2 + Om0/a + Ode0*a**2 + 1-Oall)
t = np.array([(integrate.quad(func, 0, i)[0]/H0).to('Gyr').value for i in a])

# Interpolate
degree = 9
t_seq = np.linspace(t.min(),t.max(),300).reshape(-1,1)
coefs = np.polyfit(t, a, degree)
a_seq = np.polyval(coefs, t_seq)

fig, ax = plt.subplots()
ax.scatter(t, a, s=5, c='b')
ax.scatter(t_seq, a_seq, s=1, c='r', alpha=0.5)
plt.xlabel('Billion years from Big Bang')
plt.ylabel('Scale factor')
plt.show()
