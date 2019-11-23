import datetime
import time
from copy import deepcopy
from typing import List
from os import path
from pathlib import Path

import click

import entities
from excel_exporter import write_instance_name, write_parameter_data_tsp, write_experiment_results_tsp_ga, \
    get_workbook_and_worksheet, write_experiment_results_gc_ga, write_parameter_data_gc
from usecases.genetic_algorithms.graph_coloring import ColoringManager, GeneticAlgorithmColoring, PopulationGC
from usecases.genetic_algorithms.Tour import Tour
from utils import get_all_instances, print_progress, load_graph_nodes

# just add new parameters for experimenting
TESTING_PARAMETERS = [{
        'POPULATION_SIZE': 50,
        'NUMBER_OF_GENERATIONS': 1500,
        'MUTATION_RATE': 0.05,
        'TOURNAMENT_SIZE': 10
    }]


def solve(problem: str, nodes: List[entities.Node], population_size: int, number_of_generations: int,
          mutation_rate: float, tournament_size: int) -> (Tour, int):
    if problem == 'graph_coloring':
        manager = ColoringManager()

    for node in nodes:
        manager.add_node(node)

    if problem == 'graph_coloring':
        pop = PopulationGC(manager, population_size, True)
        ga = GeneticAlgorithmColoring(manager, mutation_rate, tournament_size)

    # Evolve population for number_of_generations
    i = 0
    while i < number_of_generations:
        pop = ga.evolve_population(pop)
        print_progress((i + 1) / number_of_generations)
        i += 1

    # jump to new line
    print('')

    return ga.best_so_far


def write_parameters(problem, ws, index, param_val: dict):
    if problem == 'graph_coloring':
        write_parameter_data_gc(ws,
                                index,
                                   'PARAMETERS (POPULATION_SIZE: {}, NUMBER_OF_GENERATIONS: {}, MUTATION_RATE: {}, '
                                   'TOURNAMENT_SIZE: {})'.format(
                                    param_val['POPULATION_SIZE'],
                                    param_val['NUMBER_OF_GENERATIONS'],
                                    param_val['MUTATION_RATE'],
                                    param_val['TOURNAMENT_SIZE']))


def write_results(problem: str, ws, index: int, row: int, res, elapsed_time):
    if problem == 'graph_coloring':
        write_experiment_results_gc_ga(ws, index, row, res, elapsed_time)


@click.command()
@click.option('--instance', '-i', help='Instance to run the construction. If none provided, will go through all',
              required=False, default='0030')
@click.option('--problem', '-p', help='Probem to solve, Graph coloring', required=False,
              default='graph_coloring', type=click.Choice(['graph_coloring']))
@click.option('--run_experiments_count', '-r', help='How many times to run each instance with some configuration',
              required=False, default=3)
def main(instance: str, problem: str, run_experiments_count: int):
    # make each test run unique by a timestamp
    timestamp = str(datetime.datetime.utcnow()).replace(' ', '').replace('-', '')

    if instance:
        # if supplied by argument, solve only that instance
        instances = [instance]
    else:
        instances = get_all_instances()

    wb, ws = get_workbook_and_worksheet()

    RUNS_PER_INSTANCE = run_experiments_count

    for i, instance in enumerate(instances):
        print('Running genetic algorithm for {} on instance {}'.format(problem, instance))
        start_index = (i * RUNS_PER_INSTANCE) + 3

        write_instance_name(ws, instance, start_index, RUNS_PER_INSTANCE)

        for param_index, param_val in enumerate(TESTING_PARAMETERS):
            write_parameters(problem, ws, param_index + 1, param_val)

            j = 0
            nodes, entities.BIG_M = load_graph_nodes(instance)

            while j < RUNS_PER_INSTANCE:
                start_time = time.time()
                print('{}.) Solving {} for {} time with param {}'.format(i + 1, instance, j + 1, param_index + 1))

                res = solve(problem=problem,
                            nodes=deepcopy(nodes),
                            population_size=param_val['POPULATION_SIZE'],
                            number_of_generations=param_val['NUMBER_OF_GENERATIONS'],
                            mutation_rate=param_val['MUTATION_RATE'],
                            tournament_size=param_val['TOURNAMENT_SIZE'])

                elapsed_time = time.time() - start_time

                # write results/graph data
                row_number = j + start_index
                if param_index == 0:
                    ws['B{}'.format(row_number)] = '-'
                    ws['C{}'.format(row_number)] = '-'

                write_results(problem, ws, param_index + 1, row_number, res, elapsed_time)

                # Save the file foreach run
                Path("..\\..\\experiments\\")
                wb.save('aco_{}_{}.xlsx'.format(problem, datetime.datetime.now().strftime("%H%M%S")))

                # Print final results
                if problem == 'graph_coloring':
                    print('Number of colors: {}, conflicts: {}'.format(res.get_number_of_colors(),
                                                                       res.get_number_of_color_conflicts()))
                print('It took: {} s \n'.format(elapsed_time))
                j += 1


if __name__ == '__main__':
    main()
