"""
Find distance from Cepheids
===========================
We know that the LMC is located at a distance of 50 kpc. We have queried
SIMBAD database with this script for LMC and M31:

For LMC:
center_ra, center_dec = 80.89375, -69.75611111
diameter = 10

For M31:
center_ra, center_dec = 10.684583333333332, 41.26916666666666
diameter = 3

SELECT TOP 100 oid, main_id, mesVar.period, allfluxes.V
FROM basic
LEFT JOIN allfluxes ON basic.oid=allfluxes.oidref
LEFT JOIN mesVar ON basic.oid=mesVar.oidref
WHERE 1=CONTAINS(
POINT('ICRS', {center_ra}, {center_dec}),
CIRCLE('ICRS',ra, dec, {diameter}))
AND otype_txt='cC*'
AND allfluxes.V IS NOT NULL
AND period IS NOT NULL
ORDER BY period DESC

We have found two Cepheid variable stars with the same period, one in LMC
and the other in M31 (first row from LMC, second from M31).

  oid  |        main_id          |  period |  V   
-------|-------------------------|---------|------
3155867|"HD 269075"              |47.51    |12.48
9124054|"2MASS J00422103+4052490"|47.136892|18.86


Find our distance to M31.
"""

import numpy as np
from astropy import units as u
from astropy.constants import L_sun

def flux(m):
    '''Convert apparent magnitude to flux'''
    fx = 2.53 * (10**-8) * u.Unit('W / m2')
    f = fx * 10**(m/-2.5)
    return f

def f_d_2_L(f, d):
    '''Calculate luminosity from flux and distance'''
    L = f * 4 * np.pi * d**2
    return L

def L_f_2_d(L, f):
    '''Calculate luminosity distance from luminosity and flux'''
    d = np.sqrt(L / (4 * np.pi * f))
    return d

# know parameters
m_lmc = 12.48
m_m31 = 18.86
d_lmc = (50*u.Unit('kpc')).to('m')

#===================================================
# METHOD 1
# --------
# First we find flux of both stars
f_lmc = flux(m_lmc)
f_m31 = flux(m_m31)

# Now we find luminosity of the star in LMC
L_lmc = f_d_2_L(f_lmc, d_lmc)

# Since both stars have the same period, they have the same luminosity, too
L_m31 = L_lmc

# Now we can find the distance to the star in M31
d_m31 = L_f_2_d(L_m31, f_m31)

print(d_m31.to('pc'))

#============================================================
# METHOD 2
# --------
"""
f1 / f2 = (L1 / 4*np.pi*d1**2) / (L2 / 4*np.pi*d2**2)
Since L1 = L2 we have:
f1 / f2 = d2**2 / d1**2
=> d2 = d1 * sqrt(f1/f2)
"""

d_m31 = d_lmc * np.sqrt(flux(m_lmc)/flux(m_m31))
print(d_m31.to('pc'))
#============================================================
# METHOD 3
# --------
"""
We can use distance modulus formula (d is in pc):

M = m - 5*np.log10(d) + 5

Since L1 = L2, so M1 = M2
m1 - 5*np.log10(d1) + 5 = m2 - 5*np.log10(d2) + 5
=>
d2 = 10**((m2-m1+5*np.log10(d1)) / 5)
"""
d_lmc_pc = d_lmc.to('pc').value
d_m31_pc = 10**((m_m31-m_lmc+5*np.log10(d_lmc_pc)) / 5)

print(d_m31_pc, 'pc')
