import bspice as bs
from datetime import datetime
import os
from glob import glob

path = 'bs_kernels'

if os.path.isdir(path):
    files = glob(path + '/*')
else:
    os.mkdir(path)
    files = []

files = [i.split('\\')[-1] for i in files]

BASE = 'https://naif.jpl.nasa.gov/pub/naif/generic_kernels/'

'pck/earth_latest_high_prec.bpc'
    
dc_kernels = {
    'naif0012.tls': 'lsk/naif0012.tls',
    'earth_latest_high_prec.bpc': 'pck/earth_latest_high_prec.bpc',
    #'earth_200101_990628_predict.bpc': 'pck/earth_200101_990628_predict.bpc',
    'pck00010.tpc': 'pck/pck00010.tpc'
    }

for k,v in dc_kernels.items():
    if k not in files:
        bs.download_file(BASE+v, path=path+'/')
        print(k, 'downloaded.')

generic_kernels = [path+'/'+i for i in dc_kernels.keys()]

adr = 'C:/Moi/_py/Astronomy/Solar System/SPK/data/'
jup = adr + 'jup380s.bsp'
ss = adr + 'de440s.bsp'



kernels = generic_kernels + [jup] + [ss]


t = datetime.utcnow()

obs_loc = (7.744083817548831, 48.58313582900411, 140)

r, az, alt = bs.get_apparent(599, t, obs_loc, kernels)
print('Az :', az)
print('Alt:', alt)
print('r  :', r)
