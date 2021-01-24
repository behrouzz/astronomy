# Taken from here:
# https://learn.astropy.org/rst-tutorials/units-and-integration.html

import numpy as np
from scipy import integrate
from astropy import units as u, constants as c
import matplotlib.pyplot as plt

def bs_func(m):
    if m > 1:
        return m**-2.35
    else:
        return (1/m) * np.exp(((np.log10(m)-np.log10(0.2))**2) / (-2*(0.5)**2))


m_grid = np.logspace(-2., 2., 10000)
y_seq = [bs_func(i) for i in m_grid]
plt.loglog(m_grid, y_seq)
plt.xlabel(r'Stellar mass [$M_{\odot}$]')
plt.ylabel('Probability density')
plt.show()


# How many more M stars are there than O stars?
# ---------------------------------------------
n_m, _ = integrate.quad(bs_func, 0.08, 0.6)
n_o, _ = integrate.quad(bs_func, 15, 100)
print(n_m / n_o)



# Relative total masses for all O stars and all M stars born
# ----------------------------------------------------------
IMF_m = lambda m:  m*bs_func(m)

m_m, _ = integrate.quad(IMF_m, a=0.01, b=0.6)
m_o, _ = integrate.quad(IMF_m, a=15., b=100)

print(m_m / m_o)
