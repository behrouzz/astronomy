import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def distance(paral):
    dist = 1 / paral
    return np.abs(dist)

def abs_magnitude(m, d):
    M = m + 5 - 5*np.log10(d)
    return M

# Download data
base = "http://tapvizier.u-strasbg.fr/TAPVizieR/tap/sync?request=doQuery&lang=adql&format=json&query="
sql = 'SELECT HIP, Vmag, Plx, "B-V", SpType, "_RA.icrs", "_DE.icrs" FROM "I/239/hip_main"'
url = base + sql

r = requests.get(url).json()

meta = pd.DataFrame(r['metadata'])
cols = [i['name'] for i in r['metadata']]
df = pd.DataFrame(r['data'], columns=cols)

df = df.dropna()
df['dist'] = distance(df['Plx']/1000)
df['M'] = abs_magnitude(df['Vmag'], df['dist'])

plt.scatter(df['B-V'],df['M'], s=1, c='k')
plt.xlabel('Color Index (B-V)')
plt.ylabel('Absolute Magnitude (M)')
plt.gca().invert_yaxis()
plt.xlim((-0.5,2))
plt.show()

