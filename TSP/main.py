#%% ACO TSP Analysis

from tsp_utils import create_data, solve_GA
from tsp_utils import solve_ACO
import pants
import math
from tsp_utils import euclidean
import time
import pandas as pd
import numpy as np
from scipy.spatial import distance_matrix

time_results = []
dist_results = []
final_paths = []

numberGenerations = [20, 275]
problemSizeList = [15, 30]
index=0
for problemSize in problemSizeList:
    data_points = create_data(problemSize)

    start = time.time()
    solutions_ACO, solution_ACO = solve_ACO(data_points)
    end = time.time()
    time_ACO = end-start
    start = time.time()

    hof, stats = solve_GA(data_points, numberGenerations[index])

    end = time.time()
    time_DEAP = end-start

    time_results.append([problemSize, time_ACO, time_DEAP])
    dist_results.append([problemSize, solution_ACO.distance, hof.keys[0].values[0]])
    final_paths.append([problemSize, solution_ACO.visited, hof.items[0]])
    index +=1


time_results = np.array(time_results)
dist_results = np.array(dist_results)
#     return pop, stats, hof
#
#
# if __name__ == "__main__":
#     DEAP_Objects = main()


# results = []
# results.append(["Time", time_ACO, time_DEAP])
# results.append(["Distance", solution_ACO.distance, hof.keys[0].values[0]])
# results.append(["PATHS", solution_ACO.visited, hof.items[0]])
# print(results)