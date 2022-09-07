from datetime import datetime
import spiceypy as sp
import bspice as bs


d2r = 3.141592653589793/180
r2d = 180/3.141592653589793


t = datetime.utcnow()
obs_loc = (7.744083817548831, 48.58313582900411, 140)

adr = 'C:/Moi/_py/Astronomy/Solar System/SPK/data/'
gen = 'bs_kernels/'

kernels = [
    gen + 'naif0012.tls',
    gen + 'earth_latest_high_prec.bpc',
    gen + 'pck00010.tpc',
    adr + 'de440s.bsp',
    adr + 'jup380s.bsp'
    ]

for k in kernels:
    sp.furnsh(k)

et = sp.str2et(str(t))

#=========================================

target = 10

# Get ICRS position
state, lt = sp.spkez(targ=target,
                     et=et,
                     ref='J2000',
                     abcorr='NONE',
                     obs=0)

pos = state[:3]
vel = state[3:]

##from hypatie import mag
##print(mag(pos))

# Conversion matrix (J2000 to earth-fixed prime meridian)
m = sp.tipbod(ref='J2000', body=399, et=et)
"""
m is a 3x3 matrix that transforms positions in inertial coordinates
to positions in body-equator-and-prime-meridian coordinates.
"""


# Coordinates in earth-fixed prime meridian
new_pos = sp.mxvg(m1=m, v2=pos)
print(new_pos)
print(m.dot(pos))


# Convert from rectangular coordinates to latitudinal coordinates
r, lon, lat = sp.reclat(new_pos)
print('r  :', r)
print('lon:', lon*r2d)
print('lat:', lat*r2d)

tmp1 = bs.lonlat_to_cartesian(obs_loc)
print(tmp1)
tmp2 = sp.recazl(tmp1, azccw=False, elplsz=True)
print(tmp2)
#=========================================
sp.kclear()

"""
The transformation from Earth body-fixed frame to topocentric frame
"""
