"""
Claculating the Vernal Equinox
The instant the New Persian Year begins

By: Behrouz Safari
"""

import numpy as np
from datetime import timedelta
from astropy import coordinates as crd
from astropy.time import Time
from astropy import units as u

def eq(t, rng, unit, n):
    time_window = t + np.linspace(-rng, rng, n)*unit
    sun = crd.get_sun(time_window).tete
    decs = np.abs(np.array(sun.dec.deg))
    ind = np.argmin(decs)
    return time_window[ind]

def eq_year(yr):
    t_ini = Time(yr+'-03-20 12:00')
    t = eq(t_ini, 2, u.day, 5)
    t = eq(t, 12, u.hour, 24)
    t = eq(t, 30, u.minute, 60)
    t = eq(t, 30, u.second, 60)
    t_fin = eq(t, 500, u.ms, 1000)
    return t_fin

# Example: calculating the vernal equinox of 2021
utc = eq_year('2021')
ir = utc + timedelta(hours=3.5)

fmt = '%Y-%m-%d %H:%M:%S.%f'
print('UTC  :', utc.strftime(fmt))
print('Iran :', ir.strftime(fmt))

