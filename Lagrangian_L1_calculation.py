"""
Suppose that we have a star (s), a planet (p) and a sattelite (l).
We want to put the sattelite in the lagrangian point L1, between the
star and th planet, where the sum of gravitational forces acting on
the sattelite are zero.

L = Rsp - Rsl 

F = ( G*(Ms*Ml)/(Rsp-L)**2 ) - ( G*(Mp*Ml)/L**2 ) = 0

=>

(Ms/(Rsp-L)**2) - (Mp/L**2) = 0

We know the values of Ms, Mp, Rsp. We want to find L with respect to
these values.
"""


from sympy import symbols
from sympy.solvers import solve

Ms, Mp, Rsp, L = symbols('Ms Mp Rsp L', real=True)

expr = (Ms/(Rsp-L)**2)-(Mp/L**2)

print(solve(expr, L))

# The answer is:
# [Rsp*(Mp - sqrt(Mp*Ms))/(Mp - Ms), Rsp*(Mp + sqrt(Mp*Ms))/(Mp - Ms)]
