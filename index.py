# functions by: https://github.com/InsightLab/PyMove

import math
import os

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

def identifies_patterns(all_user_csv):
    patterns_array = []

    for csv in all_user_csv:
        arr = []
        c1 = pd.read_csv(csv)

        for coordinate in all_user_csv:
            c2 = pd.read_csv(coordinate)
            medp = MEDP(c1, c2)

            if medp > 0 and medp <= 0.015:
              arr.append(coordinate)

        if len(arr) != 0:
          arr.append(csv)
          patterns_array.append(sorted(arr))

    arrAux = []
    [arrAux.append(x) for x in patterns_array if x not in arrAux]

    return arrAux

def compare_patterns(users_identified_patterns):
  users_compared_patterns = {}
  users_compared_patterns_arr = []

  for user in users_identified_patterns:
      user_patterns = users_identified_patterns[user]

      for other_user in users_identified_patterns:
          other_user_patterns = users_identified_patterns[other_user]

          for pattern in user_patterns:
            c1 = pd.read_csv(pattern[0])

            for other_pattern in other_user_patterns:
                c2 = pd.read_csv(other_pattern[0])

                medp = MEDP(c1,c2)

                if medp > 0 and medp <= 0.015:
                    users_compared_patterns_arr.append(other_user)

      users_compared_patterns[user] = users_compared_patterns_arr
      users_compared_patterns_arr = []

  return users_compared_patterns

def run():
    Path = os.path.dirname(os.path.realpath(__file__))
    directory_list = os.listdir(f"{Path}/coordinates")

    users_identified_patterns = {}
    for directory in directory_list:
        path_csv =  f"{Path}/coordinates/{directory}/"

        all_user_csv = os.listdir(path_csv)
        all_user_csv = [path_csv + x for x in all_user_csv]

        users_identified_patterns[directory] = identifies_patterns(all_user_csv)

    users_compared_patterns = compare_patterns(users_identified_patterns)

    return users_compared_patterns

users_compared_patterns = run()
print(users_compared_patterns)
