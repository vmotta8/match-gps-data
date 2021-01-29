# functions by: https://github.com/InsightLab/PyMove

import math

import numpy as np
import pandas as pd

from scipy.spatial import distance


def nearest_points(traj1, traj2, latitude='lat', longitude='lon'):
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

def MEDP(traj1, traj2, latitude='lat', longitude='lon'):
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
c3 = pd.read_csv('coordinates/3.csv')

somaP1 = MEDP(c1, c2)
somaP2 = MEDP(c1, c3)
somaP3 = MEDP(c2, c3)

print(somaP1)
print(somaP2)
print(somaP3)
