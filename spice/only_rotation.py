import numpy as np
from scipy.spatial.transform import Rotation


v1 = np.array([[ 0, 0, 0],
               [ 0, 0, 1.220021],
               [ 1.145114, 0, -0.740403],
               [1.064686, 0.00001, -1.741278]])

v2 = np.array([[ 0 , 0 , 0 ],
               [ 0.08, 1.04, -0.63 ],
               [ 0.15, -0.07, 1.37],
               [-0.04, -0.97, 1.79]])


rt, rmsd = Rotation.align_vectors(v1, v2)

m = rt.as_matrix()
