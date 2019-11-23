import random
from typing import List


class NodeGC:
    def __init__(self, name: str, neighbors: dict):
        """Neighbors contains only the list of actual neighbors (not inexistent a.k.a bigM ones)"""
        self.name = name
        self.neighbors: List[str] = neighbors.keys()

    def __repr__(self):
        return self.name


class ColoringManager:
    def __init__(self):
        self.nodes = []

    def add_node(self, node):
        self.nodes.append(node)

    def get_node(self, index):
        return self.nodes[index]

    @property
    def number_of_nodes(self):
        return len(self.nodes)


class Coloring:
    def __init__(self, coloring_manager: ColoringManager):
        self.coloring_manager = coloring_manager
        self.assigned_colors = [None for i in range(0, coloring_manager.number_of_nodes)]
        self.initial_number_of_colors = 0

    def __len__(self):
        return len(self.assigned_colors)

    def __getitem__(self, index):
        return self.assigned_colors[index]

    def __setitem__(self, index, value):
        self.assigned_colors[index] = value

    def __repr__(self):
        return str(self.get_number_of_colors())

    def generate_individual(self):
        """Generates random initial solution"""
        num_of_colors = random.randint(1, int(self.coloring_manager.number_of_nodes / 2))
        self.initial_number_of_colors = num_of_colors

        # assign colors to the first num_of_colors vertices (this makes sure that for each color
        # there is at least one vertex with that color)
        random_first_colors = random.sample(range(1, num_of_colors + 1), num_of_colors)
        for node in range(0, num_of_colors):
            self.assigned_colors[node] = random_first_colors[node]

        for node in range(num_of_colors, self.coloring_manager.number_of_nodes):
            self.assigned_colors[node] = random.randint(1, num_of_colors)

    def get_color(self, coloring_position):
        return self.assigned_colors[coloring_position]

    def set_color(self, coloring_position, node):
        self.assigned_colors[coloring_position] = node

    def get_fitness(self):
        return 50 * self.get_number_of_colors() + 100 * self.get_number_of_color_conflicts()

    def get_number_of_colors(self):
        return len(set(self.assigned_colors))

    def get_number_of_color_conflicts(self):
        no_of_conflicts = 0

        for node_index, node in enumerate(self.coloring_manager.nodes):
            for neighbor in node.neighbors:
                if self.assigned_colors[node_index] == self.assigned_colors[int(neighbor)]:
                    no_of_conflicts += 1

        # we count the same conflict twice, so divide it up
        return int(no_of_conflicts / 2)


class PopulationGC:
    def __init__(self, coloring_manager, population_size: int, initialise: bool):
        self.colorings: List[Coloring] = [None for i in range(0, population_size)]

        if initialise:
            for i, coloring in enumerate(self.colorings):
                coloring = Coloring(coloring_manager)
                coloring.generate_individual()
                self.save_coloring(i, coloring)

    def __setitem__(self, key, value):
        self.colorings[key] = value

    def __getitem__(self, index):
        return self.colorings[index]

    def save_coloring(self, index, coloring):
        self.colorings[index] = coloring

    def get_coloring(self, index) -> Coloring:
        return self.colorings[index]

    def get_fittest(self):
        """Returns the coloring with least fitness value"""
        return sorted(self.colorings, key=lambda t: t.get_fitness())[0]

    @property
    def population_size(self):
        return len(self.colorings)


class GeneticAlgorithmColoring:
    def __init__(self, coloring_manager, mutation_rate: float, tournament_size: int):
        self.coloring_manager = coloring_manager
        self.mutation_rate = mutation_rate
        self.tournament_size = tournament_size
        self.best_so_far = None

    def evolve_population(self, pop):
        new_population = PopulationGC(self.coloring_manager, pop.population_size, False)

        for i in range(0, new_population.population_size):
            parent_1 = self.tournament_selection(pop)
            parent_2 = self.tournament_selection(pop)
            child = self.crossover(parent_1, parent_2)
            new_population.save_coloring(i, child)

            # mutate the population (if luck decides to...)
            self.mutate(new_population.get_coloring(i))

        fittest = new_population.get_fittest()
        if not self.best_so_far:
            self.best_so_far = fittest

        if self.best_so_far.get_fitness() > fittest.get_fitness():
            self.best_so_far = fittest

        return new_population

    def crossover(self, parent1, parent2):
        child = Coloring(self.coloring_manager)
        number_of_nodes = self.coloring_manager.number_of_nodes

        start_pos, end_pos = 1, 1
        # find two splitting points where start < end_pos
        while start_pos >= end_pos:
            start_pos = int(random.random() * number_of_nodes)
            end_pos = int(random.random() * number_of_nodes)

        # use 0 - start_pos from parent 1, start_pos - end_pos from parent 2, and end_pos to end use parent 1 again
        for i in range(0, number_of_nodes):
            if i < start_pos:
                child.set_color(i, parent1.get_color(i))
            elif start_pos <= i <= end_pos:
                child.set_color(i, parent2.get_color(i))
            else:
                child.set_color(i, parent1.get_color(i))

        return child

    def mutate(self, coloring):
        """Pick a random vertex and assign a new color to it"""
        # do mutation only with some probability
        if random.random() > self.mutation_rate:
            return

        chosen_node = random.randint(0, coloring.coloring_manager.number_of_nodes - 1)

        while True:
            # pick a new color for the chosen node
            new_color = random.randint(1, coloring.get_number_of_colors() + 1)

            if new_color != coloring.assigned_colors[chosen_node]:
                break
        coloring.assigned_colors[chosen_node] = new_color

    def tournament_selection(self, pop):
        tournament = PopulationGC(self.coloring_manager, self.tournament_size, False)
        for i in range(0, self.tournament_size):
            random_id = int(random.random() * pop.population_size)
            tournament.save_coloring(i, pop.get_coloring(random_id))

        fittest = tournament.get_fittest()
        return fittest
