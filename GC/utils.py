from sys import stdout
from os import path
from pathlib import Path

from entities import Node


def get_all_instances():
    """Returns the names of all instances. Note: all these instances should be available in instances directory"""
    return ['0010', '0015', '0020', '0030', '0040', '0050', '0060', '0070', '0080', '0090', '0100']


def get_all_instances_fake():
    """Returns the names of all instances. Note: all these instances should be available in instances directory"""
    return ['0010', '0015', '0020', '0030', '0040', '0050', '0060', '0070', '0080', '0090', '0100', '0150',
            '0200', '0250', '0300', '0400', '0500', '0600', '0700', '0800', '0900', '1000', '1500', '2000', '2500',
            '3000']


def print_progress(percent: float):
    # percent float from 0 to 1.
    stdout.write("\r")
    stdout.write("    {:.0f}%".format(percent * 100))
    stdout.flush()


def load_graph_nodes(instance_name: str):
    """Returns a list of nodes for the given instance and the corresponding bigM value"""
    print('Loading nodes for instance: {}'.format(instance_name))

    path_to_instances = Path('{}/{}'.format(path.dirname(__file__), 'instances'))
    filename = path_to_instances / '{}.txt'.format(instance_name)

    nodes = []
    all_positive_edges_weight = 0
    all_negative_edges_weight = 0

    with open(filename) as fp:
        lines = fp.readlines()
        # first line contains number of nodes and number of edges
        number_of_nodes = int(lines[0].split(' ')[0])

        for node in range(0, number_of_nodes):
            neighbors = {}
            for line in lines[1:]:
                # node1, node2, weight
                edge_representation = line.split(' ')

                if node == int(edge_representation[0]):
                    # add neighbor as key and weight as value
                    neighbors[edge_representation[1]] = int(edge_representation[2])

                if node == int(edge_representation[1]):
                    # add neighbor as key and weight as value
                    neighbors[edge_representation[0]] = int(edge_representation[2])

                if int(edge_representation[2]) > 0:
                    all_positive_edges_weight += int(edge_representation[2])
                else:
                    all_negative_edges_weight += int(edge_representation[2])

            nodes.append(Node(str(node), neighbors))

    # since each edge is counted twice, divide total value by two
    all_positive_edges_weight = int(all_positive_edges_weight / 2)
    all_negative_edges_weight = int(all_negative_edges_weight / 2)

    return nodes, max(all_positive_edges_weight, abs(all_negative_edges_weight))

