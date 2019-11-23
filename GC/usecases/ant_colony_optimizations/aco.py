import datetime
import time
from copy import deepcopy
from os import path
from typing import List
from pathlib import Path

import click

import entities
from entities import Node
from excel_exporter import get_workbook_and_worksheet, write_instance_name, \
    write_parameter_data_gc, write_experiment_results_gc_aco
from usecases.ant_colony_optimizations.graph_coloring import AntColonyGC
from usecases.ant_colony_optimizations.graph import Graph
from utils import get_all_instances, load_graph_nodes

TESTING_PARAMETERS = [{
        'ANT_COUNT': 200,
        'GENERATIONS': 100,
        'ALPHA': 0.5,
        'BETA': 8.0,
        'RHO': 0.5,
        'Q': 10,
        'STRATEGY': 1,
    }]
def solve_gc(nodes: List[Node], ant_count: int, generations: int, alpha: float, beta: float, rho: float,
              q: int, strategy: int):
    cost_matrix = []
    rank = len(nodes)
    for i in range(rank):
        row = []
        for j in range(rank):
            row.append(nodes[i].distance_to(nodes[j]))
        cost_matrix.append(row)
    aco = AntColonyGC(nodes, ant_count, generations, alpha, beta, rho, q, strategy)
    graph = Graph(cost_matrix, rank)
    # returns the best coloring
    return aco.solve(graph)


def write_parameters(problem, ws, index, param_val: dict):
    if problem == 'graph_coloring':
        write_parameter_data_gc(ws,
                                index,
                                'PARAMETERS (ANT_COUNT: {}, GENERATIONS: {}, ALPHA: {}, '
                                'BETA: {}, RHO: {}, Q: {}, STRATEGY: {})'.format(
                                param_val['ANT_COUNT'],
                                param_val['GENERATIONS'],
                                param_val['ALPHA'],
                                param_val['BETA'],
                                param_val['RHO'],
                                param_val['Q'],
                                param_val['STRATEGY']))


def write_results(problem: str, ws, index: int, row: int, res, elapsed_time):
    if problem == 'graph_coloring':
        write_experiment_results_gc_aco(ws, index, row, res, elapsed_time)


@click.command()
@click.option('--instance', '-i', help='Instance to run the construction. If none provided, will go through all',
              required=False, default=None)
@click.option('--problem', '-p', help='Which probem to solve. Either TSP or Graph coloring', required=False,
              default='graph_coloring', type=click.Choice(['tsp', 'graph_coloring']))
@click.option('--run_experiments_count', '-r', help='How many times to run each instance with some configuration',
              required=False, default=7)
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
        print('Running ant colony optimization for {} on instance {}'.format(problem, instance))
        start_index = (i * RUNS_PER_INSTANCE) + 3

        write_instance_name(ws, instance, start_index, RUNS_PER_INSTANCE)

        for param_index, param_val in enumerate(TESTING_PARAMETERS):
            write_parameters(problem, ws, param_index + 1, param_val)

            j = 0
            nodes, entities.BIG_M = load_graph_nodes(instance)

            while j < RUNS_PER_INSTANCE:
                start_time = time.time()
                print('{}.) Solving {} for {} time with param {}'.format(i + 1, instance, j + 1, param_index + 1))

                if problem == 'graph_coloring':
                    res = solve_gc(nodes=deepcopy(nodes),
                                   ant_count=param_val['ANT_COUNT'],
                                   generations=param_val['GENERATIONS'],
                                   alpha=param_val['ALPHA'],
                                   beta=param_val['BETA'],
                                   rho=param_val['RHO'],
                                   q=param_val['Q'],
                                   strategy=param_val['STRATEGY'])

                elapsed_time = time.time() - start_time

                # write results/graph data
                row_number = j + start_index
                if param_index == 0:
                    ws['B{}'.format(row_number)] = '-'
                    ws['C{}'.format(row_number)] = '-'

                write_results(problem, ws, param_index + 1, row_number, res, elapsed_time)
                wb.save('aco_{}.xlsx'.format(problem))

                # Print final results
                if problem == 'graph_coloring':
                    print('Number of colors: {}, conflicts: {}'.format(res.get_number_of_colors(),
                                                                      res.get_number_of_color_conflicts()))
                print('It took: {} s \n'.format(elapsed_time))
                j += 1


if __name__ == '__main__':
    main()
