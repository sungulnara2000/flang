from collections import deque


class NFA:
    start = 0
    regex = ''
    edges = {}
    def __init__(self, regex):
        if len(regex) == 1:
            self.nodes_count = 2
            self.edges = {0: [(1, regex)]}
            self.terminals = {1}
            self.start = 0
            return
        stack = deque()
        for i in regex:
            if i not in {'+', '*', '.'}:
                stack.append(NFA(i))
            elif i == '+':
                second = stack.pop()
                first = stack.pop()
                stack.append(first.plus(second))
            elif i == '*':
                stack.append(stack.pop().star())
            elif i == '.':
                second = stack.pop()
                first = stack.pop()
                stack.append(first.dot(second))
            # else:
            #     raiseError
        self.terminals = stack[0].terminals
        self.nodes_count = stack[0].nodes_count
        self.edges = stack[0].edges
        if len(self.terminals) > 1:
            for t in self.terminals:
                self.edges[t] = [(self.nodes_count, '')]
            self.terminals = {self.nodes_count}
            self.edges[self.nodes_count] = []
            self.nodes_count += 1

        self.remove_unreachable()

    def plus(self, other):
        other.edges = {x + 1: [(i[0] + 1, i[1]) for i in y] for x, y in other.edges.items()}
        self.edges = {x + other.nodes_count + 1: [(i[0] + other.nodes_count + 1, i[1]) for i in y] for x, y in self.edges.items()}
        if 0 in self.edges:
            self.edges[0].append((1, ''))
        else:
            self.edges[0] = [(1, '')]
        self.edges[0].append((other.nodes_count + 1, ''))
        self.edges.update(other.edges)
        other.terminals = set(map(lambda x: x + 1, other.terminals))
        self.terminals = set(map(lambda x: x + other.nodes_count + 1, self.terminals))
        self.terminals.update(other.terminals)
        self.nodes_count += 1 + other.nodes_count
        return self

    def star(self):
        for i in self.terminals:
            if i in self.edges:
                self.edges[i].append((0, ''))
            else:
                self.edges[i] = [(0, '')]
        return self

    def dot(self, other):
        other.edges = {(i[0] + self.nodes_count, i[1] + self.nodes_count, i[2]) for i in other.edges}
        other.terminals = set(map(lambda x: x + self.nodes_count, other.terminals))
        self.edges.update({i: (self.nodes_count, '') for i in self.terminals})
        self.edges.update(other.edges)
        self.terminals = other.terminals
        self.nodes_count += other.nodes_count
        return self

    def remove_unreachable(self):
        reachable = set()
        stack = deque()
        stack.append(self.start)
        while len(stack) > 0:
            a = stack.pop()
            reachable.add(a)
            for b, c in self.edges[a]:
                if b not in reachable:
                    stack.append(b)
        for a in range(self.nodes_count):
            if a not in reachable:
                del self.edges[a]
                self.terminals.discard(a)

    def print(self):
        print("End nodes: {ends}".format(ends=self.terminals))
        for a, b in self.edges.items():
            for x, y in b:
                print(a, ' -> ', x, ' via ', y)

    def reverse(self):
        tmp = {}
        for nfrom, lst in self.edges.items():
            for nto, symbol in lst:
                if nto in tmp:
                    tmp[nto].append((nfrom, symbol))
                else:
                    tmp[nto] = [(nfrom, symbol)]

        self.edges = tmp
        tmp = self.start
        self.start = self.terminals.pop()
        self.terminals = {tmp}