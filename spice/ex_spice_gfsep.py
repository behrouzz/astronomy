# https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/Tutorials/pdf/individual_docs/29_geometry_finder.pdf

import spiceypy as sp
import bspice as bs
from datetime import datetime

adr = 'C:/Moi/_py/Astronomy/Solar System/kernels/'

kernels = [
    adr + 'de421.bsp',
    adr + 'pck00009.tpc',
    adr + 'naif0009.tls'
    ]

MAXWIN = 1000

for k in kernels:
    sp.furnsh(k)


result = sp.stypes.SPICEDOUBLE_CELL(2*MAXWIN)
cnfine = sp.stypes.SPICEDOUBLE_CELL(2)


begtim = sp.str2et('2007-01-01 00:00:00')
endtim = sp.str2et('2007-07-01 00:00:00')

sp.wninsd(begtim, endtim, cnfine)

step = 6 * 86400


sp.gfsep(
    targ1='moon', shape1='SPHERE', inframe1='NULL',
    targ2='sun', shape2='SPHERE', inframe2='NULL',
    abcorr='NONE',
    obsrvr='earth',
    relate='LOCMAX',
    refval=0.0,
    adjust=0.0,
    step=step,
    nintvls=MAXWIN,
    cnfine=cnfine, result=result)

count = sp.wncard(result)

# results in TDB
for i in range(count):
    beg, end = sp.wnfetd(result, i)
    t1 = sp.et2datetime(beg)
    t2 = sp.et2datetime(end)
    print(t1, '|||', t2)
    

sp.kclear()

# https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gfsep_c.html
