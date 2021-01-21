"""
Period-Luminosity relation in LMC Cepheids
==========================================
We donwload three properties of Cepheid variable stars in the Large
Magellanic Cloud (LMC) from three tables of SIMBAD database:

1) basic.oid     : identifier of object (star)
2) mesVar.period : period of star in days
3) allfluxes.V   : flux in Visible filter (apparent magnitude)

We know that our distance to LMC is about 50 kpc, so we assume that our
distance to all its stars is the same value. Then, using the distance modulus
formula, we calculate the absolute magnitudes (M). Finally, we plot M vs. log
of period and we'll fit a regression line.
"""

import requests, pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import seaborn as sns
sns.set()


# LMC distance (pc)
d = 50000

base = 'http://simbad.u-strasbg.fr/simbad/sim-tap/sync?request=doQuery&lang=adql&format=json&query='

sql = """SELECT oid, mesVar.period, allfluxes.V
FROM basic
LEFT JOIN allfluxes ON basic.oid=allfluxes.oidref
LEFT JOIN mesVar ON basic.oid=mesVar.oidref
WHERE 1=CONTAINS(
POINT('ICRS', 13.18666667, -72.82861111),
CIRCLE('ICRS',ra, dec, 0.167))
AND otype_txt='cC*'
AND allfluxes.V IS NOT NULL"""
sql = sql.replace('\n', ' ')

r = requests.get(base+sql).json()
meta = pd.DataFrame(r['metadata'])
cols = [i['name'] for i in r['metadata']]
df = pd.DataFrame(r['data'], columns=cols)

df = df.groupby('oid').mean()

df['log_period'] = np.log10(df['period'])

# Absolute Magnitude
df['M'] = df['V'] - (5 * np.log10(d/10))

# ignoring outliers
#df = df[(df['log_period']>0) & (df['log_period']<1.5)]

X = df['log_period'].values.reshape(-1, 1)
y = df['M'].values.reshape(-1, 1)

reg = LinearRegression().fit(X,y)

log_per_seq = np.linspace(df['log_period'].min(), df['log_period'].max(), 300)

fig, ax = plt.subplots()
ax.scatter(df['log_period'], df['M'], s=1)
ax.scatter(log_per_seq, reg.predict(log_per_seq.reshape(-1, 1)), s=1)
ax.set_xlabel('Log of period')
ax.set_ylabel('Absolute Magnitude')
ax.invert_yaxis()
plt.title('LMC Cepheid Variable Stars')
plt.show()
