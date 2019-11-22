import math
import random
import pants
from scipy.spatial import distance_matrix


def create_data(amt_points):
    random.seed(42)
    nodes = []
    for _ in range(amt_points):
        x = random.uniform(0, 1000)
        y = random.uniform(0, 1000)
        nodes.append((x, y))
    return nodes


def euclidean(a, b):
    return math.sqrt(pow(a[1] - b[1], 2) + pow(a[0] - b[0], 2))


def solve_ACO(nodes):
    world = pants.world.World(nodes=nodes, lfunc=euclidean)
    solver = pants.Solver()
    solution = solver.solve(world)
    solutions = solver.solutions(world)
    # print(solution.distance)
    # print(solution.tour)  # Nodes visited in order
    # print(solution.path)  # Edges taken in order
    # best = float("inf")
    # for solution in solutions:
    #     assert solution.distance < best
    #     best = solution.distance
    return solutions, solution

def solve_GA(nodes, numberGenerations):
    from deap import algorithms
    from deap import base
    from deap import creator
    from deap import tools
    import array
    import random
    import json
    import numpy

    dist_matrix = distance_matrix(nodes, nodes)
    IND_SIZE = dist_matrix.shape[0]

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", array.array, typecode='i', fitness=creator.FitnessMin)

    toolbox = base.Toolbox()

    toolbox.register("indices", random.sample, range(IND_SIZE), IND_SIZE)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    def evalTSP(individual):
        #this initialization of distance ensures that the path of the last element back
        #to the first element is included in the calculation (so its a full round trip)!
        distance = dist_matrix[individual[-1]][individual[0]]
        for gene1, gene2 in zip(individual[0:-1], individual[1:]):
            distance += dist_matrix[gene1][gene2]
        return distance,

    toolbox.register("mate", tools.cxPartialyMatched)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("evaluate", evalTSP)

    # def main():
    random.seed(42)
    pop = toolbox.population(n=300)

    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    algorithms.eaSimple(pop, toolbox, 0.7, 0.2, ngen=numberGenerations, stats=stats, halloffame=hof)

    return hof, stats