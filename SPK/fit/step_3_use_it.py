import numpy as np
import pandas as pd
from datetime import datetime
import math
from julian import datetime_to_jd

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
