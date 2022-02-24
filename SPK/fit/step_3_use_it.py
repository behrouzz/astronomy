import numpy as np
import pandas as pd
from datetime import datetime
import math

data = pd.read_csv('data.csv')

domains = {(0, 10) : [2451536.5, 2469808.5],
           (0, 1) : [2451536.5, 2469808.5],
           (0, 2) : [2451536.5, 2469808.5],
           (0, 3) : [2451536.5, 2469808.5],
           (0, 4) : [2451536.5, 2469808.5],
           (0, 5) : [2451536.5, 2469808.5],
           (0, 6) : [2451536.5, 2469808.5],
           (0, 7) : [2451536.5, 2469808.5],
           (0, 8) : [2451536.5, 2469808.5],
           (3, 301) : [2451540.5, 2469808.5],
           (3, 399) : [2451540.5, 2469808.5]}


def datetime_to_jd(t):
    year = t.year
    month = t.month
    t_d = t.day
    t_H = t.hour
    t_M = t.minute
    t_S = t.second
    t_MS = t.microsecond
    day = t_d + t_H/24 + t_M/(24*60) + t_S/(24*60*60) + t_MS/(24*60*60*1000000)
    
    if month == 1 or month == 2:
        yearp = year - 1
        monthp = month + 12
    else:
        yearp = year
        monthp = month
    
    if ((year < 1582) or
        (year == 1582 and month < 10) or
        (year == 1582 and month == 10 and day < 15)):
        # before start of Gregorian calendar
        B = 0
    else:
        # after start of Gregorian calendar
        A = math.trunc(yearp / 100.)
        B = 2 - A + math.trunc(A / 4.)
        
    if yearp < 0:
        C = math.trunc((365.25 * yearp) - 0.75)
    else:
        C = math.trunc(365.25 * yearp)
        
    D = math.trunc(30.6001 * (monthp + 1))
    jd = B + C + D + day + 1720994.5
    
    return jd


def get_pos(t, target, center, data=data):
    t = datetime_to_jd(t)
    domain = domains[(center, target)]
    df = data[(data['center']==center) & (data['target']==target)]
    fx = np.polynomial.chebyshev.Chebyshev(coef=df['cfx'].values, domain=domain)
    fy = np.polynomial.chebyshev.Chebyshev(coef=df['cfy'].values, domain=domain)
    fz = np.polynomial.chebyshev.Chebyshev(coef=df['cfz'].values, domain=domain)
    pos = np.array([fx(t), fy(t), fz(t)])
    return pos

# example: current position of Earth wrt SSB
t = datetime.utcnow()
pos = get_pos(t, 3, 0)
print(pos)


