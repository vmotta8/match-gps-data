import pymove
import pymove.utils as utils
move_df_points = pymove.read_csv('points.csv')
move_df_pp = pymove.read_csv('pp.csv')

somaP = utils.distances.MEDP(move_df_pp, move_df_points)
somaT = utils.distances.MEDT(move_df_pp, move_df_points)
print(somaP)
print(somaT)

#
