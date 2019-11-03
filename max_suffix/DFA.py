from NFA import reversedNFA
from collections import deque


class reversedDFA(reversedNFA):
    def __init__(self, regex):
        super(reversedDFA, self).__init__(regex)
        new_terminals = set()
        new_edges = {}
        # find epsilon-closure for each node
        self.eps_closure = {}
        self.states = []
        for node in range(self.nodes_count):
            self.calc_eps_closure(node)

        stack = deque()
        self.start = self.eps_closure[self.start]
        stack.append(self.start)
        while len(stack) > 0:
            cur_state = stack.pop()
            if cur_state not in self.states:
                self.states.append(cur_state)
                for symbol in self.alphabet:
                    new_state = self.find_next(cur_state, symbol, new_edges)
                    if len(new_state) > 0:
                        stack.append(new_state)

        for i in range(len(self.states)):
            if self.states[i].intersection(self.terminals):
                new_terminals.add(frozenset(self.states[i]))
        self.terminals = new_terminals
        self.edges = new_edges

    def calc_eps_closure(self, node):
        stack = deque()
        used = set()
        stack.append(node)
        while len(stack) > 0:
            cur = stack.pop()
            used.add(cur)
            if cur in self.edges:
                for next_by_eps in [i[0] for i in self.edges[cur] if i[1] == '' and i[0] not in used]:
                    stack.append(next_by_eps)
        self.eps_closure[node] = frozenset(used)

    def find_next(self, state, symbol, new_edges):
        state = frozenset(state)
        next = set()
        for nfrom in state:
            for b, c in self.edges.get(nfrom, []):
                if c == symbol:
                    next.update(self.eps_closure[b])
        if len(next) > 0:
            new_edges[(state, symbol)] = frozenset(next)
        return next

    def print_dfa(self):
        print("End nodes: {ends}".format(ends=self.terminals))
        for a, b in self.edges.items():
                print(a[0], ' -> ', b, ' via ', a[1])

    def find_max_pref(self, word):
        # max_len = 0
        # cur = self.start
        # next = self.edges.get((cur, word[max_len]), [])
        # while len(next) > 0 and max_len < len(word) - 1:
        #     max_len += 1
        #     next = self.edges.get((next, word[max_len]), [])
        # return max_len + 1
        max_len = 0
        cur = self.start
        for i in word:
            cur = self.edges.get((cur, i), [])
            if len(cur) > 0:
                max_len += 1
            else:
                break
        return max_len
