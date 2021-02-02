import numpy as np
from astropy import units as u
from astropy.constants import G, M_sun, M_earth
from astropy.coordinates import SkyCoord, get_body_barycentric
from astropy.time import Time

def dist(p, P):
    x1,y1,z1 = p
    x2,y2,z2 = P
    return np.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)

def f(p,P):
    '''Vector of gravitational force'''
    d = dist(p,P)
    mag_f = (G*M_earth*M_sun)/(d**2)
    x,y,z = p
    X,Y,Z = P
    
    d_xy = np.sqrt((Y-y)**2 + (X-x)**2)
    # d / d_xy = F / F_xy => F_xy =...
    f_xy = (mag_f * d_xy) / d
    teta = np.arctan((Y-y)/(X-x))
    fx = f_xy * np.cos(teta)
    
    d_xz = np.sqrt((Z-z)**2 + (X-x)**2)
    # d / d_xz = F / F_xz => F_xz =...
    f_xz = (mag_f * d_xz) / d
    teta = np.arctan((X-x)/(Z-z))
    fz = f_xz * np.cos(teta)

    d_yz = np.sqrt((Z-z)**2 + (Y-y)**2)
    # d / d_yz = F / F_yz => F_yz =...
    f_yz = (mag_f * d_yz) / d
    teta = np.arctan((Z-z)/(Y-y))
    fy = f_yz * np.cos(teta)
    
    return (fx,fy,fz)


def position(planet, t):
    c = SkyCoord(get_body_barycentric(planet, t)).cartesian
    return (c.x.to('m'), c.y.to('m'), c.z.to('m'))

def velocity(planet):
    p1 = position(planet, t1)
    p2 = position(planet, t2)
    vx = (p2[0] - p1[0]) / dt
    vy = (p2[1] - p1[1]) / dt
    vz = (p2[2] - p1[2]) / dt
    return (vx,vy,vz)

# Initial conditions
t1 = Time.now()
dt = 1 * u.s
t2 = t1 + dt

pe0 = position('earth', t1)
ps0 = position('sun', t1)

ve = velocity('earth')
vs = velocity('sun')

d0 = dist(pe0, ps0)
print(f(pe0, ps0))
