import bspice as bs
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np

obs_loc = (7.744083817548831, 48.58313582900411, 140)

#adr = 'C:/Moi/_py/Astronomy/Solar System/kernels/'
adr = 'C:/Users/H21/Desktop/Desktop/Behrouz/Astronomy/kernels/'

kernels = [adr+i for i in bs.main_kernels]
kernels = kernels + [adr+'de440_2030_earth_sun_moon.bsp']

t1 = datetime(2022, 9, 10)
t2 = datetime(2022, 9, 11)

t = np.array([t1+timedelta(seconds=i) for i in range(86400)])

r_az_alt = bs.get_apparent_window(10, t1, t2, 86400,
                                  obs_loc, kernels, abcorr='LT+S')

alt = r_az_alt[:,-1]
i_noon = np.where(alt==max(alt))
a = abs(alt)
i1 = np.where(a==min(a))
a[i1] = np.nan
i2 = np.where(a==min(a))

if i1<i2:
    i_rise = i1
    i_set = i2
else:
    i_rise = i2
    i_set = i1

print('Rise:', t[i_rise][0], 'UTC')
print('Noon:', t[i_noon][0], 'UTC')
print('Set :', t[i_set][0], 'UTC')

fig, ax = plt.subplots()
ax.scatter(t, alt, s=1, alpha=0.5)
ax.scatter(t[i_rise], alt[i_rise], s=30, c='green')
ax.scatter(t[i_noon], alt[i_noon], s=30, c='orange')
ax.scatter(t[i_set], alt[i_set], s=30, c='red')
plt.grid()
plt.show()
