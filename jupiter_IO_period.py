from hypatie.horizons import download

# Approching : 2021-05-21 : -2351618.1732786293
# Receding   : 2021-11-16 : 2335495.1735259728

def get_script(correction, t1, t2):
    script = f"""
    MAKE_EPHEM=YES
    COMMAND=501
    EPHEM_TYPE=VECTORS
    CENTER='500@399'
    START_TIME='{t1}'
    STOP_TIME='{t2}'
    STEP_SIZE='1 MINUTES'
    VEC_TABLE='1'
    REF_SYSTEM='ICRF'
    REF_PLANE='FRAME'
    VEC_CORR='{correction}'
    OUT_UNITS='KM-S'
    VEC_LABELS='NO'
    VEC_DELTA_T='NO'
    CSV_FORMAT='YES'
    OBJ_DATA='NO'
    """
    return script

download(get_script('NONE', '2021-05-19', '2021-05-23')).to_csv('approch_geo.csv')
download(get_script('LT'  , '2021-05-19', '2021-05-23')).to_csv('approch_ast.csv')
download(get_script('NONE', '2021-11-14', '2021-11-18')).to_csv('reced_geo.csv')
download(get_script('LT'  , '2021-11-14', '2021-11-18')).to_csv('reced_ast.csv')

#===========================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def prepare(df):
    df['TBD'] = pd.to_datetime(df['TBD'])
    df.set_index('TBD', inplace=True)
    pos = df[['X','Y','Z']].values
    dist = [np.linalg.norm(i) for i in pos]
    df['d'] = dist
    return df

def get_period(df):
    df = prepare(df)
    
    t = df['JDTDB'].values
    d = df['d'].values
    
    coef = np.polyfit(t, d, 1)
    trend = t*coef[0] + coef[1]
    cont = d - trend

    peaks, _ = find_peaks(cont, height=200000)
    peak_times = t[peaks]
    periods = peak_times[1:] - peak_times[:-1]
    period = periods.mean()

    return df, t, peaks, periods, period
    
# Approaching
geos = get_period(pd.read_csv('approch_geo.csv'))
asts = get_period(pd.read_csv('approch_ast.csv'))

geo, t, geo_peaks, geo_periods, geo_period = geos
ast, _, ast_peaks, ast_periods, ast_period = asts

print('Approaching geometric period   :', geo_period)
print('Approaching astrometric period :', ast_period)

# Receding
geos = get_period(pd.read_csv('reced_geo.csv'))
asts = get_period(pd.read_csv('reced_ast.csv'))

geo, t, geo_peaks, geo_periods, geo_period = geos
ast, _, ast_peaks, ast_periods, ast_period = asts

print('Receding geometric period      :', geo_period)
print('Receding astrometric period    :', ast_period)

