from NFA import reversedNFA
from DFA import reversedDFA


def main():
    # reversedNFA('ab + c.∗')
    dfa = reversedDFA('acb..bab.c. ∗ .ab.ba. + . + ∗a.')
    dfa.print_dfa()
    word = 'cbaa'
    answer = dfa.find_max_pref(word[::-1])
    print(answer)

if __name__ == "__main__":
    main()