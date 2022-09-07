import bspice as bs
from datetime import datetime

kernels = ['data/naif0012.tls',
           #'data/earth_latest_high_prec.bpc',
           'data/earth_200101_990628_predict.bpc',
           'data/de440s.bsp',
           'data/pck00010.tpc',
           'C:/Users/H21/Desktop/Desktop/Behrouz/Astronomy/SPK/bsp_files/jup310.bsp'
           ]

t = datetime.utcnow()

obs_loc = (7.744083817548831, 48.58313582900411, 140)

r, az, alt = bs.get_apparent(10, t, obs_loc, kernels)
print('Az :', az)
print('Alt:', alt)
print('r  :', r)
