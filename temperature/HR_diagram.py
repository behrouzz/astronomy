"""
             source_id       plx       dist          g          b          r
0  5420219624853996672  0.428503  2877.6820  13.380870  14.008046  12.522399
1  5420219732228461184  1.319803   943.5892  10.039055  10.084611   9.924967
2  5420219732233481472  0.511638        NaN  16.105730        NaN        NaN
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('gaia_hip.csv')
df = df[df['plx']>0]

df['B_R'] = df['b'] - df['r']

d = 1 / (df['plx'].values/1000)

df['M'] = df['g'].values - 5 * np.log10(d) + 5

fig, ax = plt.subplots()
ax.scatter(df['B_R'], df['M'], s=1)
ax.invert_yaxis()
plt.show()
