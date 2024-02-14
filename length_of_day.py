from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from urllib.request import urlretrieve

def eop62(file=None):
    if file is None:
        file = 'eopc04_IAU2000.62-now'
        URL = 'https://hpiers.obspm.fr/iers/eop/eopc04/' + file
    if not os.path.isfile(file):
        print(f'Downloading {file}...')
        urlretrieve(URL, file)

    with open(file, 'r') as f:
        data = f.read().split('\n')[14:]

    data = [i[:88] for i in data]

    dates = []
    mjd = []
    x = []
    y = []
    dut1 = []
    lod = []
    dx = []
    dy = []
    for line in data[:-1]:
        ls = [i.strip() for i in line.split(' ') if len(i)>0]
        dates.append(datetime(int(ls[0]), int(ls[1]), int(ls[2])))
        mjd.append(int(ls[3]))
        x.append(float(ls[4]))
        y.append(float(ls[5]))
        dut1.append(float(ls[6]))
        lod.append(float(ls[7]))
        dx.append(float(ls[8]))
        dy.append(float(ls[9]))
        
    df = pd.DataFrame({'t': dates, 'mjd':mjd,
                       'x':x, 'y':y, 'dut1':dut1,
                       'lod':lod, 'dx':dx, 'dy':dy})
    return df

df = eop62()

##t1 = datetime(2022, 1, 1)
##t2 = datetime(2023, 1, 1)
##df = df[(df['t']>=t1) & (df['t']<t2)]

lod_ms = df['lod'].values * 1000 #milliseconds
dates = df['t'].values

print('Shortest day:', dates[np.argmin(lod_ms)])
print('Longest  day:', dates[np.argmax(lod_ms)])

plt.plot(dates, lod_ms, lw=0.5)
plt.scatter(dates, lod_ms, s=5)
plt.title('Length Of Day faster/slower than 24h\n- : shorter than 24h (fast)\n+ : longer than 24h (slow)')
plt.xlabel('Date')
plt.ylabel('Faster than 86400s (milliseconds)')
plt.grid()
plt.show()
