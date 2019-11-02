class Automata:
    terminals = {}
    nodes_count = 0
    edges = {}
    start = 0

    def star(self):
        raise NotImplementedError("Star is * sign, should be implemented for automata")

    def plus(self, other):
        raise NotImplementedError("+ should be defined for automata")

    def dot(self, other):
        raise NotImplementedError("concatination should be defined for automata")

