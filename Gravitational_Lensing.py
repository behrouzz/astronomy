# page 198 pdf

import numpy as np
import astropy.units as u
from astropy.constants import c, G, M_sun, R_sun, M_earth, R_earth

def sch(M):
    '''Schwarzschild radius'''
    rs = (2*G*M) / c**2
    return rs

def angle(M, R):
    '''deflect angle'''
    a = (4 * G * M) / (c**2 * R)
    return a * u.Unit('rad')

print('Sun deflects photons by angle  :', angle(M_sun, R_sun).to('arcsec'))
print('Earth deflects photons by angle:', angle(M_earth, R_earth).to('arcsec'))

print('\nIf Sun becomes a black hole...')
rs_sun = sch(M_sun)
print('Schwarzschild radius of Sun:', rs_sun)
print('It will deflects photons by angle:', angle(M_sun, rs_sun).to('deg'))
