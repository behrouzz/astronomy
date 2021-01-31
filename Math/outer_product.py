"""
Dyad (outer) product
====================
In constructing a dyad product from two vectors, we form the term-by-term
product of each of their individual components and add.

The result is a dyad (rank 2 tensor)

U = u1.i + u2.j + u3.k
V = v1.i + v2.j + v3.k

UV = u1.v1.ii + u1.v2.ij + u1.v3.ik + u2.v1.ji + ···

Note that the dyad product is neither a dot nor a cross product.
"""

from sympy.physics.vector import vprint, ReferenceFrame, outer, cross
from sympy import symbols

N = ReferenceFrame('N')

a,b,c,d,e,f = symbols('a b c d e f')

U = a*N.x + b*N.y + c*N.z
V = d*N.x + e*N.y + f*N.z

# Dyad product of vectors U and V
d = outer(U, V)
vprint(d)

# Matrix of scalar components of the dyad product
vprint(d.to_matrix(N))
