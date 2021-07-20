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

print(d.to('Mpc'))

