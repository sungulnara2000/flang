from NFA import NFA
from DFA import DFA


def main():
    # nfa = NFA('ab.')
    # print(nfa.start)
    # nfa.reverse()
    # nfa.print()
    # dfa = DFA('ab.', nfa)
    # answer = dfa.find_max_pref('bb')
    # print(answer)
    NFA("ab+").print()
    DFA("ab+", NFA("ab+")).print()

if __name__ == "__main__":
    main()