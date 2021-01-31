import numpy as np
from sympy.physics.vector import vprint, ReferenceFrame, outer


# With Sympy
# ===================================================
N = ReferenceFrame('N')

U = 3*N.x + 2*N.y + 5*N.z
V = 4*N.x - 7*N.y + 2*N.z

# Dyad product of vectors U and V
d = outer(U, V)
vprint(d)

# Matrix of scalar components of the dyad product
vprint(d.to_matrix(N))


# With Numpy
# ===================================================
A = np.array([3,  2, 5])
B = np.array([4, -7, 2])

print(np.outer(A,B))
