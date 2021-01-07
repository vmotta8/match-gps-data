import math

import numpy as np
import pandas as pd
from scipy.spatial import distance

from pymove import utils
from pymove.utils.constants import DATETIME, EARTH_RADIUS, LATITUDE, LONGITUDE

def nearest_points(traj1, traj2, latitude=LATITUDE, longitude=LONGITUDE):
    """
    For each point on a trajectory, it returns the point closest to
    another trajectory based on the Euclidean distance.

    Parameters
    ----------
    traj1: dataframe
        The input of one trajectory.

    traj2: dataframe
        The input of another trajectory.

    latitude: string ("lat" by default)
        Label of the trajectories dataframe referring to the latitude.

    longitude: string ("lon" by default)
        Label of the trajectories dataframe referring to the longitude.
    """

    result = pd.DataFrame(columns=traj1.columns)

    for i in range(0, len(traj1)):
        round_result = np.Inf
        round_traj = []
        for j in range(0, len(traj2)):
            this_distance = distance.euclidean(
                (traj1[latitude].iloc[i], traj1[longitude].iloc[i]),
                (traj2[latitude].iloc[j], traj2[longitude].iloc[j]),
            )
            if this_distance < round_result:
                round_result = this_distance
                round_traj = traj2.iloc[j]
        result = result.append(round_traj)

    return result

def MEDP(traj1, traj2, latitude=LATITUDE, longitude=LONGITUDE):
    """
    Returns the Mean Euclidian Distance Predictive between
    two trajectories, which considers only the spatial
    dimension for the similarity measure.

    Parameters
    ----------
    traj1: dataframe
        The input of one trajectory.

    traj2: dataframe
        The input of another trajectory.

    latitude: string ("lat" by default)
        Label of the trajectories dataframe referring to the latitude.

    longitude: string ("lon" by default)
        Label of the trajectories dataframe referring to the longitude.
    """

    soma = 0
    traj2 = nearest_points(traj1, traj2, latitude, longitude)

    # if(len(traj2) < len(traj1)):
    #     traj1, traj2 = traj2, traj1

    for i in range(0, len(traj1)):
        this_distance = distance.euclidean(
            (traj1[latitude].iloc[i],
             traj1[longitude].iloc[i]),
            (traj2[latitude].iloc[i],
             traj2[longitude].iloc[i]))
        soma = soma + this_distance
    return soma

c1 = pd.read_csv('coordinates/1.csv')
c2 = pd.read_csv('coordinates/2.csv')

somaP = MEDP(c1, c2)
print(somaP)
