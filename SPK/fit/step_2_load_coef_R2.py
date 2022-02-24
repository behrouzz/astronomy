from jplephem.spk import SPK
import numpy as np
import pandas as pd
from julian import datetime_to_jd, jd_to_datetime
from datetime import datetime, timedelta

domains = {
    (0, 10) : [2451536.5, 2469808.5],
    (0, 1) : [2451536.5, 2469808.5],
    (0, 2) : [2451536.5, 2469808.5],
    (0, 3) : [2451536.5, 2469808.5],
    (0, 4) : [2451536.5, 2469808.5],
    (0, 5) : [2451536.5, 2469808.5],
    (0, 6) : [2451536.5, 2469808.5],
    (0, 7) : [2451536.5, 2469808.5],
    (0, 8) : [2451536.5, 2469808.5],
    (3, 301) : [2451540.5, 2469808.5],
    (3, 399) : [2451540.5, 2469808.5]
}


def get_func(df, center, target, domain):
    df = df[(df['center']==center) & (df['target']==target)]
    fx = np.polynomial.chebyshev.Chebyshev(coef=df['cfx'].values, domain=domain)
    fy = np.polynomial.chebyshev.Chebyshev(coef=df['cfy'].values, domain=domain)
    fz = np.polynomial.chebyshev.Chebyshev(coef=df['cfz'].values, domain=domain)
    return fx, fy, fz

def compare(t, fx, fy, fz, kernel, center, target):
    t = datetime_to_jd(t)
    pos_pred = np.array([fx(t), fy(t), fz(t)]) # predict
    pos_real = kernel[center,target].compute(t) # real
    diff = pos_real - pos_pred
    return pos_real, pos_pred, diff

def R2(x, y, y_pred):
    x, y, y_pred = np.array(x), np.array(y), np.array(y_pred)
    res = y - y_pred
    ss_res = np.sum(res**2)
    ss_tot = np.sum((y - np.mean(y))**2)
    return 1 - (ss_res / ss_tot)

df = pd.read_csv('data.csv')
kernel = SPK.open('de421.bsp')

for k in domains.keys():
    dom = domains[k]
    center = k[0]
    target = k[1]
    fx, fy, fz = get_func(df, center, target, dom)

    # define time window
    t0 = datetime(2010,1,1)
    tn = datetime(2040,1,1)
    N = (tn-t0).days

    ts = []
    xs = []
    ys = []
    zs = []
    xs_pred = []
    ys_pred = []
    zs_pred = []
    
    for i in range(0, N, 10):
        t = t0 + timedelta(days=i)
        pos_real, pos_pred, diff = compare(t, fx, fy, fz, kernel, center, target)
        ts.append(t)
        xs.append(pos_real[0])
        ys.append(pos_real[1])
        zs.append(pos_real[2])
        xs_pred.append(pos_pred[0])
        ys_pred.append(pos_pred[1])
        zs_pred.append(pos_pred[2])

    # R2
    print(k)
    print('R2 X :', R2(ts, xs, xs_pred))
    print('R2 Y :', R2(ts, ys, ys_pred))
    print('R2 Z :', R2(ts, zs, zs_pred))
    print('-'*50)

kernel.close()






