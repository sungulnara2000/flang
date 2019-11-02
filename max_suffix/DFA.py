from NFA import NFA
from collections import deque


class DFA:
    def __init__(self, regex, nfa):
        self.alphabet = set(regex) - set("+.*")
        self.terminals = set()
        self.old_edges = {nfrom: [(nto, symbol) for i, nto, symbol in nfa.edges if i == nfrom] for nfrom in range(nfa.nodes_count)}
        self.edges = {}
        # find epsilon-closure for each node
        self.eps_closure = {}
        self.states = []
        for node in range(nfa.nodes_count):
            self.calc_eps_closure(node)

        stack = deque()
        self.start = self.eps_closure[nfa.start]
        stack.append(self.start)
        while len(stack) > 0:
            cur_state = stack.pop()
            if cur_state not in self.states:
                self.states.append(cur_state)
                for symbol in self.alphabet:
                    new_state = self.find_next(cur_state, symbol)
                    if len(new_state) > 0:
                        stack.append(new_state)

        for i in range(len(self.states)):
            if self.states[i].intersection(nfa.terminals):
                self.terminals.add(frozenset(self.states[i]))

    def calc_eps_closure(self, node):
        stack = deque()
        used = set()
        stack.append(node)
        while len(stack) > 0:
            cur = stack.pop()
            used.add(cur)
            for next_by_eps in [i[0] for i in self.old_edges[cur] if i[1] == '' and i[0] not in used]:
                stack.append(next_by_eps)
        self.eps_closure[node] = frozenset(used)

    def find_next(self, state, symbol):
        state = frozenset(state)
        next = set()
        for nfrom in state:
            for b, c in self.old_edges[nfrom]:
                if c == symbol:
                    next.update(self.eps_closure[b])
        if len(next) > 0:
            self.edges[(state, symbol)] = frozenset(next)
        return next

    def print(self):
        print("End nodes: {ends}".format(ends=self.terminals))
        for a, b in self.edges:
            print(a, ' -> ', self.edges[(a, b)], ' via ', b)

    def find_max_pref(self, word):
        max_len = 0
        cur = self.start
        next = self.edges[(cur, word[max_len])]
        while len(next) > 0 and max_len < len(word):
            next = self.edges.get((next, word[max_len]), [])
            max_len += 1
        return max_len




