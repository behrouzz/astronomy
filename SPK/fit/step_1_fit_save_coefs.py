from jplephem.spk import SPK
import numpy as np
import pandas as pd
from julian import datetime_to_jd, jd_to_datetime
from datetime import datetime

# First, download the file (de421.bsp), then open it
k = SPK.open('de421.bsp')

segments = [(0,10), (0,1), (0,2), (0,3), (0,4), (0,5), (0,6), (0,7), (0,8),
            (3,301), (3,399)]

data = []

for i in segments:
    seg = k[i[0],i[1]]
    t_ini, interval, coefficients = seg.load_array()
    t_fin = t_ini + coefficients[0,:,0].shape[0]*interval
    t = np.arange(t_ini, t_fin, interval)

    # my selection window
    d1 = datetime_to_jd(datetime(2000,1,1))
    d2 = datetime_to_jd(datetime(2050,1,1))

    ind1, = np.where(t==t[t>=d1][0])
    ind2, = np.where(t==t[t<=d2][-1])

    t_sel = t[ind1[0]-1 : ind2[0]+2]

    x,y,z = seg.compute(t_sel)
    
    N = t_sel.shape[0] # number of data points

    fx = np.polynomial.Chebyshev.fit(t_sel, x, deg=N)
    fy = np.polynomial.Chebyshev.fit(t_sel, y, deg=N)
    fz = np.polynomial.Chebyshev.fit(t_sel, z, deg=N)

    coefs = [fx.coef, fy.coef, fz.coef]
    domain = fx.domain

    print((i[0],i[1]), ':', fx.domain)

    data.append([(i[0],i[1]), {'cfx':fx.coef, 'cfy':fy.coef, 'cfz':fz.coef}])

k.close()

df_total = pd.DataFrame(columns=['center', 'target', 'cfx', 'cfy', 'cfz'])

for i in data:
    center, target = i[0]
    dc = i[1]
    df = pd.DataFrame(dc)
    df['center'] = center
    df['target'] = target
    df = df[['center', 'target', 'cfx', 'cfy', 'cfz']]
    df_total = df_total.append(df, ignore_index=True)

df_total.set_index('center').to_csv('data.csv')

# We should save these domains:
"""
(0, 10) : [2451536.5 2469808.5]
(0, 1) : [2451536.5 2469808.5]
(0, 2) : [2451536.5 2469808.5]
(0, 3) : [2451536.5 2469808.5]
(0, 4) : [2451536.5 2469808.5]
(0, 5) : [2451536.5 2469808.5]
(0, 6) : [2451536.5 2469808.5]
(0, 7) : [2451536.5 2469808.5]
(0, 8) : [2451536.5 2469808.5]
(3, 301) : [2451540.5 2469808.5]
(3, 399) : [2451540.5 2469808.5]
"""
