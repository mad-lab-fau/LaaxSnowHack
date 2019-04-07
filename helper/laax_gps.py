import pickle
from pathlib import Path

import gpxpy
import numpy as np
import pandas as pd
import requests
from geopy import distance

# The ids for (hopefully all slops in Laax) to query the OpenSnow API with it
LAAX_IDS = [132148, 132149, 132151, 132152, 132154, 132155, 132156, 132157, 132158, 132159, 132160, 132161, 132162,
            132164, 132165, 132166, 132167, 132168, 132169, 132170, 132171, 132172, 132173, 132174, 132178, 132179,
            132180, 132181, 132182, 132183, 132185, 132186, 132187, 132188, 132189, 132198, 132287, 132298, 132300,
            132301, 132302, 132303, 132305, 132320, 132321, 132339, 132340, 132341, 132343, 132344, 132421, 133043,
            154975, 168459, 189209, 199172, 199173, 199174, 199175, 199178, 207441, 207443, 207446, 207474, 207475,
            207478, 207479, 207480, 207481, 207482, 207519, 207520, 207579, 216958, 217149, 217919, 218343, 218344,
            218345]


def get_slope_info(lid):
    slope = requests.get('https://tiles.skimap.org/features/{}.geojson'.format(lid)).json()

    headers = {
        'Content-Type': 'application/json',
    }

    data = np.array(slope['geometry']['coordinates'])[:, ::-1]
    pair_dist = calc_distance_from_geo_series(data)

    elevation = requests.post('https://elevation.racemap.com/api', headers=headers, json=data.tolist()).json()
    return_data = dict()
    return_data['name'] = slope['properties']['name']
    return_data['difficulty'] = slope['properties']['piste:difficulty']
    return_data['type'] = slope['properties']['piste:type']
    return_data['id'] = slope['properties']['lid']
    return_data['overall_elevation'] = elevation[0] - elevation[-1]
    return_data['distance'] = np.sum(pair_dist)
    return_data['pos'] = np.cumsum(pair_dist)
    return_data['geo'] = data
    return_data['elevation'] = elevation
    return return_data


def calc_distance_from_geo_series(series):
    d_start = series[0]
    pairwise_dist = []

    for d_stop in series[1:]:
        pairwise_dist.append(distance.distance(d_start, d_stop).m)
        d_start = d_stop
    return pairwise_dist


def get_all_laax_slopes(force=False):
    path = Path('./output/laax_slopes.pk')
    if path.is_file() and force is not True:
        slopes = pickle.load(path.open('rb'))
    else:
        slopes = {}

    for i in LAAX_IDS:
        if i not in slopes:
            slopes[i] = get_slope_info(i)

    pickle.dump(slopes, path.open('wb'))
    return slopes


def get_gps_track(file_path):
    gpx = gpxpy.parse(open(file_path, 'r'))
    points = gpx.tracks[0].segments[0].points
    geo_track = np.array(
        [((p.time - points[0].time).total_seconds(), p.latitude, p.longitude, p.elevation) for p in points])
    return pd.DataFrame(geo_track, columns=['t', 'la', 'lo', 'el'])
