import random
from typing import List



class Tour:
    def __init__(self, tour_manager, tour=None):
        self.tour_manager = tour_manager
        self.tour = tour if tour else [None for i in range(0, self.tour_manager.number_of_nodes)]
        self.distance = 0

    def __len__(self):
        return len(self.tour)

    def __getitem__(self, index):
        return self.tour[index]

    def __setitem__(self, key, value):
        self.tour[key] = value

    def __repr__(self):
        return ' '.join([t.name for t in self.tour])

    def generate_individual(self):
        for node_index in range(0, self.tour_manager.number_of_nodes):
            self.set_node(node_index, self.tour_manager.get_node(node_index))
        random.shuffle(self.tour)

    def get_node(self, tour_position):
        return self.tour[tour_position]

    def set_node(self, tour_position, node):
        self.tour[tour_position] = node

        # reset distances so that they will be calculated on next fetch
        self.distance = 0

    def get_fitness(self):
        return abs(self.get_distance())

    def get_distance(self):
        if self.distance == 0:
            tour_distance = 0
            for node_index, node in enumerate(self.tour):
                destination_node = self.tour[(node_index + 1) % self.tour_size]
                tour_distance += node.distance_to(destination_node)

            self.distance = tour_distance

        return self.distance

    @property
    def tour_size(self):
        return len(self.tour)

    def contains_node(self, node):
        return node in self.tour





