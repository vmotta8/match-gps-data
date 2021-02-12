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

#def identifies_patterns(locales):
    #for locale in locales:
        #path1 = pd.read_csv(locale)
 
def identifies_patterns(all_user_csv):
    arr = []
    arrAux = []
    for csv in all_user_csv:
        path = pd.read_csv(csv)
        arr.append(path)
    x = 0
    for i in range(len(arr)):
        for j in range(len(arr)):
            medp = MEDP(arr[i],arr[j])  
            if medp > 0 and medp <= 0.005:
                arrAux.append(arr[i])

    if not arrAux:
        return "não há dado padronizado"
    return arrAux

"""def identifies_patterns(all_user_csv):
    for csv in all_user_csv:
        print(csv)"""
    


def run():
    Path = os.path.dirname(os.path.realpath(__file__))
    directory_list = os.listdir(f"{Path}/coordinates")

    users_identified_patterns = {}
    for directory in directory_list:
        path_csv =  f"{Path}/coordinates/{directory}/"

        all_user_csv = os.listdir(path_csv)
        all_user_csv = [path_csv + x for x in all_user_csv]

        users_identified_patterns[directory] = identifies_patterns(all_user_csv) # implementar função

        print (users_identified_patterns)
        print()
        #users_compared_patterns = compare_patterns(users_identified_patterns) # implementar função

        #return users_compared_patterns

run()
    

'''
função identifies_patterns()
   recebe um array com a localização de vários csvs e retorna um dict com o usuário e a localização das suas rotas padronizadas

   - recebe (['path/User0/1.csv', 'path/User0/2.csv', 'path/User0/3.csv', 'path/User0/4.csv', 'path/User0/5.csv', 'path/User0/6.csv', 'path/User0/7.csv', 'path/User0/8.csv', 'path/User0/9.csv', 'path/User0/10.csv'])

   - retorna { User0: ['path/User0/3.csv', 'path/User0/4.csv', 'path/User0/5.csv', 'path/User0/6.csv'], ['path/User0/9.csv', 'path/User0/10.csv']}


   - recebe (['path/User1/1.csv', 'path/User1/2.csv', 'path/User1/3.csv', 'path/User1/4.csv'])

   - retorna { User1: ['path/User1/3.csv', 'path/User1/4.csv']}



 função compare_patterns()
   recebe dict com todos os usuários e seus padrões de rotas e retorna um dict com todos os usuários com um array dos usuários que tem o mesmo padrão de rota deles

   - recebe ({ User0: ['path/User0/3.csv', 'path/User0/4.csv', 'path/User0/5.csv', 'path/User0/6.csv'], ['path/User0/9.csv', 'path/User0/10.csv'], User1: ['path/User1/3.csv', 'path/User1/4.csv']})

   - retorna ({ User0: [ User1 ], User1: [ User 0 ]})
'''
