BASE='https://simbad.u-strasbg.fr/simbad/sim-tap/sync?request=doQuery&lang=adql&format=csv&query='
url=$BASE$(sed 's/ /%20/g' <<< $1)
curl -L -s $url | csvlook
