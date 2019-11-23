BIG_M = None


class Node:
    def __init__(self, name: str, neighbors: dict):
        """Neighbors contains only the dict of actual neighbors (not inexistent a.k.a bigM ones)"""
        self.name = name
        self.neighbors = neighbors

    def distance_to(self, other):
        """Return the distance to node. If it does not exist, return bigM value"""
        return self.neighbors.get(other.name, BIG_M)

    def __repr__(self):
        return self.name
