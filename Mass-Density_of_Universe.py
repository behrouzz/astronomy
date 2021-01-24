# Pages 182-184

from astropy.constants import M_sun, L_sun
from astropy import units as u


# Luminosity of Sun in V-band
Lv_sun = 0.12 * L_sun

# Luminosity density of local universe (out to 0.1*c/H0)
lum_den = 1.1 * 10**8 * (Lv_sun / u.Unit('Mpc3'))

"""
Experimental studies show that the average mass-to-light ratio in the
local universe is:

< M / Lv > = 4 * ( M_sun / Lv_sun )

So, we can find the mass density of stars in the local universe:

den_stars = < M / Lv > * lum_den
          = (4 * M_sun / Lv_sun) * lum_den
"""
den_stars = (4 * M_sun / Lv_sun) * lum_den

# Mass density of stars in terms of mass of Sun
print(den_stars / M_sun)
