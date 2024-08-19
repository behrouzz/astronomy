import erfa
from datetime import datetime
import numpy as np
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt


def get_tt(t):
    utc1, utc2 = erfa.dtf2d('UTC', t.year, t.month, t.day, t.hour, t.minute, t.second + (t.microsecond / 1e6))
    tai1, tai2 = erfa.utctai(utc1, utc2)
    tt1, tt2 = erfa.taitt(tai1, tai2)
    return tt1, tt2

def get_cirs(rc, dc, t):
    tt1, tt2 = get_tt(t)
    ri, di, _ = erfa.atci13(rc, dc, 0, 0, 0, 0, tt1, tt2)
    return ri*erfa.DR2D, di*erfa.DR2D


data = """
star,radec
Regulus,152.092962438 11.967208776
Denebola,177.264909756 14.572058065
Algieba,154.993127333 19.841485219
Zosma,168.527089266 20.523718139
Epsilon Leonis,146.46280673687792 23.77425377711222
Adhafera,154.17256318434792 23.41731698899111
Eta Leonis,151.83313496465667 16.762663324555
Chertan,168.56002362722833 15.42957108642444
Rasalas,148.190904223595 26.00695118609
"""    

df = pd.read_csv(StringIO(data))
df['ra'] = df['radec'].str.split(' ').str[0].astype(float)
df['dec'] = df['radec'].str.split(' ').str[1].astype(float)
del df['radec']

t = datetime(2024, 8, 19)

tt1, tt2 = get_tt(t)

# sun
astrom, eo = erfa.apci13(tt1, tt2)
sunGCRS = -astrom[2]*astrom[3]
raG, decG, _ = erfa.p2s(sunGCRS)
ra_sun, dec_sun = erfa.atciqz(raG, decG, astrom)
ra_sun = ra_sun * erfa.DR2D
dec_sun = dec_sun * erfa.DR2D

# stars
ra_stars = np.zeros((len(df),))
dec_stars = np.zeros((len(df),))
for ii in range(len(df)):
    ra_stars[ii], dec_stars[ii] = get_cirs(df['ra'].iloc[ii]*erfa.DD2R, df['dec'].iloc[ii]*erfa.DD2R, t)


fig, ax = plt.subplots()
ax.scatter(ra_stars, dec_stars, s=2, c='b')
ax.scatter(ra_sun, dec_sun, s=5, c='r')
plt.gca().set_aspect('equal')
plt.show()
