"""
SELECT Source, HIP, Gmag, BPmag, RPmag, Teff
FROM "I/355/gaiadr3"
WHERE (HIP IS NOT NULL)
AND (Teff IS NOT NULL)
"""

import pandas as pd
#from sklearn.linear_model import LinearRegression, SGDRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

df = pd.read_csv('gaia_hip.csv')

# blue, green, red
df['G_B'] = df['Gmag'] - df['BPmag']
df['R_G'] = df['RPmag'] - df['Gmag']
df['R_B'] = df['RPmag'] - df['BPmag']

#X = df[['Gmag', 'BPmag', 'RPmag']].values
X = df[['G_B', 'R_G', 'R_B', 'Gmag', 'RPmag', 'BPmag']].values
y = df['Teff'].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.33, random_state=42)

model = RandomForestRegressor()

model.fit(X_train, y_train)

score = model.score(X_test, y_test)
print(score)
# ['G_B', 'R_G', 'R_B', 'Gmag'] : 0.6447005820438643
# ['G_B', 'R_G', 'R_B', 'Gmag', 'RPmag', 'BPmag']: 0.6690421583329298
