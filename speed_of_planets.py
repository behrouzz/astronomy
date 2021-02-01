"""
Speed of planets
================
Speed of planets (and the Sun) around the barycentre of the
Solar System
"""

import numpy as np
from astropy import units as u
from astropy.coordinates import SkyCoord, get_body_barycentric
from astropy.time import Time

t = Time.now()

def speed(planet, t1):
    dt = 1 * u.s
    t2 = t1 + dt
    
    c1 = SkyCoord(get_body_barycentric(planet, t1)).cartesian
    c2 = SkyCoord(get_body_barycentric(planet, t2)).cartesian
    
    vx = (c2.x.to('m') - c1.x.to('m')) / dt
    vy = (c2.y.to('m') - c1.y.to('m')) / dt
    vz = (c2.z.to('m') - c1.z.to('m')) / dt
    
    speed = np.sqrt(vx**2+vy**2+vz**2)
    return speed

planets = ['sun','mercury','venus','earth','mars','jupiter',
           'saturn','uranus','neptune']
for i in planets:
    sp = (8-len(i))*' '
    print(f'Speed of {i}{sp}: {speed(i,t):.2f}')
