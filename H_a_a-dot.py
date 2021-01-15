"""
Calculating the Hubble parameter from scale factor:

H = a_dot / a

where,

H     : Hubble parameter as a function of t
a     : scale factor as a function of t
a_dot : derivative of the scale factor with respect to t
"""

import matplotlib.pyplot as plt
from astropy.cosmology import Planck13 as cosmo
from astropy.cosmology import z_at_value
from astropy.constants import c
import numpy as np
import pandas as pd

t0 = cosmo.age(0)

t = np.linspace(0, t0, 100)[1:-1]
z = [z_at_value(cosmo.age, i) for i in t]

a = cosmo.scale_factor(z)
a_dot = np.gradient(a, t[1]-t[0]) # derivative of a with respect to t

h_calculated = (a_dot / a).to('km / (Mpc s)')
H = cosmo.H(z)

df = pd.DataFrame({'t':t, 'a':a, 'a_dot':a_dot, 'h calculé':h_calculated, 'H':H})

print(df)

fig, ax = plt.subplots()
ax.scatter(t, a, s=1, c='b') # a
ax.scatter(t, a_dot, s=1, c='r') # derivative of a
plt.xlabel('t')
plt.show()
