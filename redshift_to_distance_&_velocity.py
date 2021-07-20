import numpy as np
from astropy.constants import c
from astropy.cosmology import Planck18 as cosmo

# We want to calculate the distance of NGC 1087 with z=0.00508

z = 0.00508
a_e = 1 / (1+z) # scale factor when photons emitted

H0 = cosmo.H0

# formula from here:
# https://phys.libretexts.org/Courses/University_of_California_Davis/UCD%3A_Physics_156_-_A_Cosmology_Workbook/A_Cosmology_Workbook/08._The_Distance-Redshift_Relation

d = (c / H0) * (np.log(1)-np.log(a_e))

print('Distance of NGC 1087 :', d.to('Mpc'))

#========================================
"""
import matplotlib.pyplot as plt

zs = np.linspace(0, 0.005, 1000)
ds = (c / H0) * (np.log(1)-np.log(1/(1+zs)))
ds = ds.to('Mpc').value

plt.plot(ds, zs)
plt.xlabel('Distance (Mpc)')
plt.ylabel('Redshift (z)')
plt.grid()
plt.show()
"""
##############################

# convert redshift to velocity
# ----------------------------
# z = sqrt((c+v)/(c-v)) - 1
"""
from sympy.solvers import solve
from sympy import Symbol, sqrt

c = Symbol('c', real=True, positive=True, constant=True)
v = Symbol('v', real=True)
z = Symbol('z', real=True)

expr = z - (sqrt((c+v)/(c-v)) - 1)

velocity = solve(expr, v)
print(velocity)
"""
# ============================

from astropy.constants import c

z = 0.00508
vel = c*((z + 1)**2 - 1)/((z + 1)**2 + 1)
print('Velocity of NGC 1087 :', vel.to('km / s'))
print('Assert H0 is correct :', (vel/d).to('km / (Mpc s)'))
