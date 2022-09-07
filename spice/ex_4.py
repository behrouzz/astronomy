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

bodies = [0, 1, 2, 3, 4, 5, 6, 7, 8]

icrs_arr = np.zeros((len(bodies),3))
topo_arr = np.zeros((len(bodies),3))

for i in range(len(bodies)):
    icrs_arr[i,:] ,_ ,_ = bs.get_icrs(bodies[i], t, kernels)
    topo_arr[i,:] = bs.get_topocentric(bodies[i], t, obs_loc, kernels)


# transformation matrix from ICRS to TOPOCENTRIC
from scipy.spatial.transform import Rotation
rt, rmsd = Rotation.align_vectors(icrs_arr, topo_arr)
m = rt.as_matrix()

def get_mat_angle(translation=None, rotation=None, rotation_center=np.array([0., 0, 0])):
    mat1 = np.eye(4)
    mat2 = np.eye(4)
    mat3 = np.eye(4)
    mat1[:3, 3] = -rotation_center
    mat3[:3, 3] = rotation_center
    if translation is not None:
        mat3[:3, 3] += translation
    if rotation is not None:
        mat2[:3, :3] = Rotation.from_rotvec(np.array([0, 0, 1.]) * rotation).as_dcm()
    return np.matmul(np.matmul(mat3, mat2), mat1) 
icrs,_,_ = bs.get_icrs(599, t, kernels)
topo = bs.get_topocentric(599, t, obs_loc, kernels)
