import joblib
import numpy as np


def get_teff(model, g, r, b, plx):
    G_B = g - b
    R_G = r - g
    R_B = r - b
    x = np.array([[G_B, R_G, R_B, g, r, b, plx]])
    return model.predict(x)[0]



model = joblib.load("teff_RF_model.joblib")

# example:
g, r, b, plx = 7.937663, 7.928717, 7.922188, 3.879689

y_pred = get_teff(model, g, r, b, plx)
print(y_pred)
