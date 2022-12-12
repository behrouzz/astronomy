import numpy as np
import pandas as pd
from hypatie.catalogues import Catalogue
from hypatie.transform import equ2ecl


cat = Catalogue(name='hipparcos', where='Vmag < 5', n_max=10000)
df, meta = cat.download()

df = df[['HIP', '_RA_icrs', '_DE_icrs', 'Vmag', 'Plx']]

ra_dec_r = []
for i, row in df.iterrows():
    r = (1 / (row['Plx']*1000)) * 30856775814913.67
    ra_dec_r.append(np.array([row['_RA_icrs'], row['_DE_icrs'], r]))
    

pos_ecl = [equ2ecl(i) for i in ra_dec_r]

df['ecl_lat'] = [i[1] for i in pos_ecl]
df['abs_ecl_lat'] = abs(df['ecl_lat'])
df = df.sort_values(by='abs_ecl_lat')
df = df[df['abs_ecl_lat']<10]
del df['abs_ecl_lat']

df.set_index('HIP').to_csv('hip5_ecliptic.csv')
