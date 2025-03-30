import erfa
import iers
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

def jd_to_dt(jd):
    # faster than jd_to_datetime
    if jd < 2299160.5:
        jd -= 10
    mjd = jd - 2400000.5
    t0 = datetime(1858, 11, 17, 0)
    dt = t0 + timedelta(days=mjd)
    return dt

def get_tt(t):
    utc1, utc2 = erfa.dtf2d('UTC', t.year, t.month, t.day, t.hour, t.minute, t.second + (t.microsecond / 1e6))
    tai1, tai2 = erfa.utctai(utc1, utc2)
    tt1, tt2 = erfa.taitt(tai1, tai2)
    return tt1, tt2


def get_row(t):
    """
    Get row of sin, cos and tan of all fundamental factors
    t : centuries since J2000
    """
    # mean anomaly of the Moon.
    a1 = erfa.fal03(t)

    # mean anomaly of the Sun.
    a2 = erfa.falp03(t)

    # mean elongation of the Moon from the Sun.
    a3 = erfa.fad03(t)

    # mean longitude of the Moon minus mean longitude of the ascending node.
    a4 = erfa.faf03(t)

    # mean longitude of the Moon's ascending node.
    a5 = erfa.faom03(t)

    # general accumulated precession in longitude.
    a6 = erfa.fapa03(t)


    # mean longitude of Mercury.
    p1 = erfa.fame03(t)

    # mean longitude of Venus.
    p2 = erfa.fave03(t)

    # mean longitude of Earth.
    p3 = erfa.fae03(t)

    # mean longitude of Mars.
    p4 = erfa.fama03(t)

    # mean longitude of Jupiter.
    p5 = erfa.faju03(t)

    # mean longitude of Saturn.
    p6 = erfa.fasa03(t)

    # mean longitude of Uranus.
    p7 = erfa.faur03(t)

    # mean longitude of Neptune.
    p8 = erfa.fane03(t)

    planets = ['Mercury', 'Venus', 'Earth', 'Mars',
               'Jupiter', 'Saturn', 'Uranus', 'Neptune']
    aa = [a1, a2, a3, a4, a5, a6]
    pp = [p1, p2, p3, p4, p5, p6, p7, p8]

    funds = aa + pp

    sins = []
    coss = []
    tans = []
    for i in funds:
        sins.append(np.sin(i))
        coss.append(np.cos(i))
        tans.append(np.tan(i))

    row = sins + coss# + tans
    return row

##t0 = datetime.utcnow()
##tt1, tt2 = get_tt(t0)
##t = ((tt1 - erfa.DJ00) + tt2) / erfa.DJC


eop = iers.EOP(2)
df = eop.table
df['t'] = df['mjd'].apply(lambda x: jd_to_dt(x + 2400000.5))
df.set_index('t', inplace=True)
#df = df.loc['2000':]

##plt.plot(df.index.values, df['lod'].values)
##plt.show()

X = np.zeros((len(df), 28))

for i, mjd in enumerate(df['mjd']):
    t = ((2400000.5 - erfa.DJ00) + mjd) / erfa.DJC
    X[i, :] = get_row(t)
y = df['lod'].values.reshape(-1, 1)
#y = df['ut1_utc'].diff().fillna(0).values.reshape(-1, 1)


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

reg = LinearRegression()
reg.fit(X_train, y_train)

y_pred = reg.predict(X_test)
score = reg.score(X_test, y_test)
print(score)

for i, v in enumerate(reg.coef_[0]):
    print(i+1, ':', v)

y_ = reg.predict(X)
fig, ax = plt.subplots()
ax.plot(df.index.values, y, c='b')
ax.plot(df.index.values, y_, c='r')
plt.show()

# note: X[:,19] has very powerfull effect
