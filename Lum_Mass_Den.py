from astropy.constants import M_sun, L_sun
from astropy import units as u


Lv_sun = 0.12 * L_sun

lum_den = (1.1 * 10**8 * Lv_sun) / 1*u.Unit('Mpc')

"""
M / Lv = 4 * M_sun / Lv_sun

=>

den_stars = (M / Lv) * lum_den
          = (4 * M_sun / Lv_sun) * lum_den
"""
den_stars = (4 * M_sun / Lv_sun) * lum_den

print(den_stars / M_sun)
