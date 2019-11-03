from collections import deque


class reversedNFA:
    start = 0
    regex = ''
    edges = {}
    alphabet = {}
    def __init__(self, regex):
        self.regex = regex
        regex = regex.replace(' ', '')
        self.alphabet = set(regex) - set('+.∗')
        if len(regex) == 1 and regex not in {'+', '.', '∗'}:
            self.simple_NFA(regex)
        else:
            stack = deque()
            for i in regex:
                if i == '+':
                    if len(stack) < 2:
                        raise ValueError('Bad input. Few arguments.')
                    second = stack.pop()
                    first = stack.pop()
                    stack.append(first.plus(second))
                elif i == '∗':
                    if len(stack) < 1:
                        raise ValueError('Bad input. Few arguments.')
                    stack.append(stack.pop().star())
                elif i == '.':
                    if len(stack) < 2:
                        raise ValueError('Bad input. Few arguments.')
                    second = stack.pop()
                    first = stack.pop()
                    stack.append(first.dot(second))
                else:
                    stack.append(reversedNFA(i))
            if len(stack) > 1:
                raise ValueError('Bad input. Few operators.')
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
            self.reverse()

    def simple_NFA(self, symbol):
        if symbol not in {'a', 'b', 'c', '1'}:
            raise ValueError("Bad symbol: ", symbol)
        if symbol == '1':
            symbol = ''
        self.nodes_count = 2
        self.edges = {0: [(1, symbol)], 1: []}
        self.terminals = {1}
        self.start = 0
        return self

    def plus(self, other):
        other.start += 1
        other.edges = {x + 1: [(i[0] + 1, i[1]) for i in y] for x, y in other.edges.items()}
        self.start += other.nodes_count + 1
        self.edges = {x + other.nodes_count + 1: [(i[0] + other.nodes_count + 1, i[1]) for i in y] for x, y in self.edges.items()}
        self.edges[0] = [(other.start, '')]
        self.edges[0].append((self.start, ''))
        self.edges.update(other.edges)
        self.start = 0
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
        self.terminals = {self.start}
        return self

    def dot(self, other):
        other.start += self.nodes_count
        other.edges = {x + self.nodes_count: [(i[0] + self.nodes_count, i[1]) for i in y] for x, y in other.edges.items()}
        other.terminals = set(map(lambda x: x + self.nodes_count, other.terminals))
        for i in self.terminals:
            self.edges[i].append((other.start, ''))
        # self.edges.update({i: [(other.start, '')] for i in self.terminals})
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
            for b in self.edges[a]:
                if b[0] not in reachable:
                    stack.append(b[0])
        for a in range(self.nodes_count):
            if a not in reachable:
                del self.edges[a]
                self.terminals.discard(a)

    def print(self):
        print("End nodes: {ends}\nStart nodes: {start}".format(ends=self.terminals, start=self.start))
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