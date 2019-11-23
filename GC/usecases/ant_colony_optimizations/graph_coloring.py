import random


class Ant:
    def __init__(self):
        self.xCoord = 0
        self.yCoord = 0


class AntColonyGC:
    def __init__(self, solution, number_of_ants, number_of_cycles, alpha, beta, rho, q, strategy):
        if number_of_ants > len(solution):
            number_of_ants = len(solution)

        self.number_of_ants = number_of_ants
        self.number_of_cycles = number_of_cycles
        self.random_move_chance = 200
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.q = q
        self.strategy = strategy
        self.ant_list = []

        for i in range(0, number_of_ants):
            self.ant_list.append(Ant())

    def solve(self, solution):
        def determine_num_of_conflicting_nodes(solution):
            conflicting_num = 0
            for y_list in solution.node_list:
                for each_node in y_list:
                    for i in each_node.connected_node_list:
                        if i.color == each_node.color:
                            conflicting_num += 1

            return conflicting_num

        def determine_num_of_local_conflicts(node):
            local_conflicts = 0
            for i in node.connected_node_list:
                if i.color == node.color or node.color == 0 or i.color == 0:
                    local_conflicts += 1

            return local_conflicts

        def change_color_of_node(node):
            color_different = False
            while not color_different:
                new_color = random.randrange(1, 4)
                if node.color == new_color:
                    pass
                else:
                    node.color = new_color
                    color_different = True

        def move_ant(solution, ant):
            neighboring_nodes = []
            neighboring_nodes.extend(solution.nodeList[int(ant.xCoord / 6)][int(ant.yCoord / 6)].connectedNodeList)

            nodes_to_remove = []

            for i in neighboring_nodes:
                for g in self.ant_list:
                    if g.xCoord == i.xCoord and g.yCoord == i.yCoord:
                        nodes_to_remove.append(i)

            for each_node in nodes_to_remove:
                try:
                    neighboring_nodes.remove(each_node)
                except:
                    pass

            if not neighboring_nodes:
                pass
            else:
                node_choice = random.randrange(0, len(neighboring_nodes))
                ant.xCoord = neighboring_nodes[node_choice].xCoord
                ant.yCoord = neighboring_nodes[node_choice].yCoord

        for ant in self.ant_list:
            ant_location_unique = False
            while not ant_location_unique:
                randX = random.randrange(0, len(solution.node_list))
                randY = random.randrange(0, len(solution.node_list[randX]))

                test_x_coord = solution.nodeList[randX][randY].xCoord
                test_y_coord = solution.nodeList[randX][randY].yCoord

                ant_conflict = 0
                for each_ant in self.ant_list:
                    if each_ant.xCoord == test_x_coord and each_ant.yCoord == test_y_coord:
                        ant_conflict = 1

                if ant_conflict == 0:
                    ant_location_unique = True

                    ant.xCoord = test_x_coord
                    ant.yCoord = test_y_coord

        display_delay = self.display_delay
        display_counter = display_delay

        current_cycle = 1
        cycles_to_run = self.number_of_cycles

        solution_solved = False
        while not solution_solved and cycles_to_run > 0:
            if display_counter >= display_delay:

                display_counter = 0

                if solution.is_solution_state():
                    solution_solved = True

                for ant in self.ant_list:
                    if solution.isSolutionState():
                        solution_solved = True

                    current_node = solution.nodeList[int(ant.xCoord / 6)][int(ant.yCoord / 6)]

                    num_of_local_conflicts = determine_num_of_local_conflicts(current_node)

                    if num_of_local_conflicts == 0:
                        pass
                    else:
                        change_color_of_node(current_node)

                    # Process ant movement
                    move_ant(solution, ant)

                # Iterate cycle counters
                current_cycle += 1
                cycles_to_run -= 1
            else:
                display_counter += 1

        return current_cycle
