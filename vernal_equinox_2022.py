from datetime import datetime
from requests import request
import pandas as pd
from hypatie.data import cities


BASE_URL = 'https://ssd.jpl.nasa.gov/horizons_batch.cgi?batch=1&'

def get_script(loc, h1, h2):
    script = f"""
    MAKE_EPHEM=YES
    COMMAND=10
    EPHEM_TYPE=OBSERVER
    CENTER='coord@399'
    COORD_TYPE=GEODETIC
    SITE_COORD='{loc}'
    START_TIME='2022-03-20 {h1}'
    STOP_TIME='2022-03-20 {h2}'
    STEP_SIZE='1000'
    QUANTITIES='2'
    REF_SYSTEM='ICRF'
    CAL_FORMAT='CAL'
    TIME_DIGITS='FRACSEC'
    ANG_FORMAT='DEG'
    APPARENT='AIRLESS'
    RANGE_UNITS='AU'
    SUPPRESS_RANGE_RATE='NO'
    SKIP_DAYLT='NO'
    SOLAR_ELONG='0,180'
    EXTRA_PREC='NO'
    RTS_ONLY='NO'
    CSV_FORMAT='NO'
    OBJ_DATA='YES'
    """
    return script


def get_t(loc, h1, h2):
    script = get_script(loc, h1, h2)
    url = BASE_URL + script
    error_msg = ''
    req = request('GET', url)
    all_text = req.content.decode('utf-8')
    if ('$$SOE' not in all_text) or ('$$EOE' not in all_text):
        error_msg = all_text[:all_text.find('$$SOF')]
        print(error_msg)
    mark1 = all_text.find('$$SOE')
    text = all_text[mark1+6:]
    mark2 = text.find('$$EOE')
    text = text[:mark2]
    raw_rows = text.split('\n')[:-1]
    head = all_text[:mark1]
    raw_rows = [i.strip() for i in raw_rows]
    times = [i[:24] for i in raw_rows]
    dec = [float(i[-8:]) for i in raw_rows]
    dec = [abs(i) for i in dec]
    df = pd.DataFrame({'t':times, 'dec':dec})
    df['t'] = df['t'].apply(lambda i: datetime.strptime(i, '%Y-%b-%d %H:%M:%S.%f'))
    rec = df[df['dec']==df['dec'].min()]
    t = rec['t'].iloc[0]
    return t


dc = {}
for i in cities.keys():
    tmp = cities[i]
    if tmp[0]>0:
        lon = '+' + str(tmp[0])
        
    if tmp[1]>0:
        lat = '+' + str(tmp[1])

    el = str(tmp[2]/1000)
    dc[i] = lon+','+lat+','+el

# example
city = 'washington'
t = get_t(dc[city], '15:35', '15:45')
print(city.title(), ':', t)
