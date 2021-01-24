# Pages 182-185
"""
Experimental studies show that the average mass-to-light ratio in the
local universe is:

< M / Lv > = 4 * ( M_sun / Lv_sun )

So, we can find the mass density of stars in the local universe:

mass_den = < M / Lv > * lum_den
          = (4 * M_sun / Lv_sun) * lum_den
"""

import numpy as np
from astropy.constants import M_sun, L_sun, c, G
from astropy import units as u
from astropy.cosmology import Planck13 as cosmo


# Luminosity of Sun in V-band
Lv_sun = 0.12 * L_sun

# Luminosity density of local universe (out to 0.1*c/H0)
lum_den = 1.1 * 10**8 * (Lv_sun / u.Unit('Mpc3'))

# Mass density of stars
mass_den = (4 * M_sun / Lv_sun) * lum_den
print('Mass density of stars:', mass_den)

H0 = cosmo.H(0).to('1/s')

# Current critical energy density of universe
ced0 = ((3 * c**2) / (8 * np.pi * G)) * H0**2

# Current critical mass density of universe (E=MC2)
cmd0 = (ced0 / (c**2)).to('kg / Mpc3')
print('Current critical mass density of universe:', cmd0)

# Density parameter of stars
den_par = mass_den / cmd0
print('Density parameter of stars:', den_par)
