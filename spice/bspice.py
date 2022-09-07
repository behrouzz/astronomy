"""
Useful kernels:
---------------
https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/naif0012.tls
https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/earth_200101_990628_predict.bpc
https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/pck00010.tpc

https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de440s.bsp

#https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/earth_latest_high_prec.bpc
#https://naif.jpl.nasa.gov/pub/naif/generic_kernels/fk/planets/earth_assoc_itrf93.tf
"""

import spiceypy as sp
import requests
from glob import glob
import numpy as np



d2r = 3.141592653589793/180
r2d = 180/3.141592653589793


def download_file(url, path=''):
    filename = url.rsplit('/', 1)[-1]
    r = requests.get(url, allow_redirects=True)
    open(path+filename, 'wb').write(r.content)
    

def lonlat_to_cartesian(obs_loc):
    """
    obs_loc : (lon (deg), lat (deg), alt (m))
    """
    lon, lat, alt = obs_loc
    lon = lon * d2r
    lat = lat * d2r
    alt = alt / 1000
    radii = [6378.1366, 6378.1366, 6356.7519]
    re = radii[0]
    rp = radii[2]
    f = (re-rp)/re
    obspos = sp.pgrrec(body='earth', lon=lon, lat=lat, alt=alt, re=re, f=f)
    return obspos


def get_icrs(body, t, kernels):
    for k in kernels:
        sp.furnsh(k)
    et = sp.str2et(str(t))
    state, lt = sp.spkez(targ=body, et=et, ref='J2000', abcorr='NONE', obs=0)
    pos = state[:3]
    vel = state[3:]
    sp.kclear()
    return pos, vel, lt


def get_topocentric(body, t, obs_loc, kernels):
    r,az,alt = get_apparent(body, t, obs_loc, kernels, abcorr='NONE')
    for k in kernels:
        sp.furnsh(k)
    topo = sp.azlrec(range=r, az=az*d2r, el=alt*d2r,
                     azccw=False, elplsz=True)
    sp.kclear()
    return topo


def get_apparent(body, t, obs_loc, kernels, abcorr='LT+S'):

    if isinstance(body, int):
        body = str(body)

    for k in kernels:
        sp.furnsh(k)

    et = sp.str2et(str(t))
    
    state, lt  = sp.azlcpo(
        method='ELLIPSOID',
        target=body,
        et=et,
        abcorr=abcorr,
        azccw=False,
        elplsz=True,
        obspos=lonlat_to_cartesian(obs_loc),
        obsctr='earth',
        obsref='ITRF93')

    r, az, alt = state[:3]

    sp.kclear()

    return r, az*r2d, alt*r2d


def ecef2enu_rot(obs_loc):
    lon, lat, _ = obs_loc
    lon = lon * d2r
    lat = lat * d2r
    r1 = [-np.sin(lon), np.cos(lon), 0]
    r2 = [-np.cos(lon)*np.sin(lat), -np.sin(lon)*np.sin(lat), np.cos(lat)]
    r3 = [np.cos(lon)*np.cos(lat), np.sin(lon)*np.cos(lat), np.sin(lat)]
    return np.array([r1, r2, r3])

