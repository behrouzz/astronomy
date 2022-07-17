# Goto Gaia Tap service: https://gea.esac.esa.int/archive/
# Run this script and download results as 'gaia_hip.csv'
"""
SELECT 
hip.source_id, 
sl.parallax AS plx, 
sl.phot_g_mean_mag AS g, 
sl.phot_bp_mean_mag AS b, 
sl.phot_rp_mean_mag AS r, 
sl.teff_gspphot AS teff

FROM gaiadr3.hipparcos2_best_neighbour as hip

LEFT JOIN gaiadr3.gaia_source_lite AS sl
ON hip.source_id=sl.source_id

WHERE (hip.angular_distance < 0.005) AND (hip.number_of_neighbours=1) AND (sl.teff_gspphot IS NOT NULL)
"""

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

df = pd.read_csv('gaia_hip.csv')

df['G_B'] = df['g'] - df['b']
df['R_G'] = df['r'] - df['g']
df['R_B'] = df['r'] - df['b']

X = df[['G_B', 'R_G', 'R_B', 'g', 'r', 'b', 'plx']].values
y = df['teff'].values

X_train, X_test, y_train, y_test = train_test_split(X, y)

model = RandomForestRegressor()

model.fit(X_train, y_train)

score = model.score(X_test, y_test)
print(score)
# 0.80

joblib.dump(model, "teff_RF_model.joblib")
