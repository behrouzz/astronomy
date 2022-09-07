from datetime import datetime
import spiceypy as sp
import bspice as bs
import numpy as np


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

#========================
for k in kernels:
    sp.furnsh(k)
et = sp.str2et(str(t))
state, lt = sp.spkez(targ=10, et=et, ref='J2000', abcorr='NONE', obs=399)
pos_icrs = state[:3]
vel = state[3:]
#sp.kclear()
#========================

TSIPM = sp.tisbod(ref='J2000', body=399, et=et)

pos_itrf = np.matmul(TSIPM[:3,:3], pos_icrs)

sp.kclear()


R = bs.ecef2enu_rot(obs_loc)

enu_pos = np.matmul(R, pos_itrf)

from hypatie.transform import car2sph

a = car2sph(enu_pos)
print('Az  :', a[0])
print('Alt :', a[1])
print('dist:', a[2]/149597870.70000002)


