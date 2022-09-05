"""
https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/naif0012.tls
https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/earth_200101_990628_predict.bpc
https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/pck00010.tpc

https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de440s.bsp

#https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/earth_latest_high_prec.bpc
#https://naif.jpl.nasa.gov/pub/naif/generic_kernels/fk/planets/earth_assoc_itrf93.tf
"""

import spiceypy as sp
from datetime import datetime
from hypatie import mag

d2r = 3.141592653589793/180
r2d = 180/3.141592653589793

def get_apparent(body, t, obs_loc, kernels, abcorr='LT+S'):

    if isinstance(body, int):
        body = str(body)

    lon, lat, alt = obs_loc

    lon = lon * d2r
    lat = lat * d2r
    alt = alt / 1000

    for k in kernels:
        sp.furnsh(k)

    et = sp.str2et(str(t))

    dim, values = sp.bodvrd(bodynm="earth", item="RADII", maxn=3)

    re  =  values[0]
    rp  =  values[2]
    f   =  ( re - rp ) / re

    # lonlat to cartesian
    obspos = sp.pgrrec(body='earth', lon=lon, lat=lat, alt=alt, re=re, f=f)

    state, lt  = sp.azlcpo(
        method='ELLIPSOID',
        target=body,
        et=et,
        abcorr=abcorr,
        azccw=False,
        elplsz=True,
        obspos=obspos,
        obsctr='earth',
        obsref='ITRF93')

    r, az, alt = state[:3]

    sp.kclear()

    return r, az*r2d, alt*r2d


kernels = ['data/naif0012.tls',
           #'data/earth_latest_high_prec.bpc',
           'data/earth_200101_990628_predict.bpc',
           'data/pck00010.tpc',
           'data/de440s.bsp',
           'C:/Users/H21/Desktop/Desktop/Behrouz/Astronomy/SPK/bsp_files/jup310.bsp'
           ]

t = datetime(2022, 9, 1)

obs_loc = (7.744083817548831, 48.58313582900411, 140)

r, az, alt = get_apparent(501, t, obs_loc, kernels)
print('Az :', az)
print('Alt:', alt)
print('r  :', r)
