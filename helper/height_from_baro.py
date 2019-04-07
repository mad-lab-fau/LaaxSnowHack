import numpy as np


def height_from_baro(baro, ref_altitudes=None):
    altitude = 44330 * (1.0 - (baro / 1013.0) ** 0.1903)
    if ref_altitudes:
        alt_diffs = list()
        for lift in ref_altitudes:
            alt_diffs.append(ref_altitudes[lift][0] - altitude[int(ref_altitudes[lift][1]*200)])

        altitude = altitude + np.mean(alt_diffs)

    return altitude
