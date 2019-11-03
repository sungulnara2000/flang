from DFA import reversedDFA

class Test:
    regexs = ['ab + c.aba. ∗ .bac. + . + ∗', 'acb..bab.c. ∗ .ab.ba. + . + ∗a.']
    words = ['babc', 'cbaa']
    answers = [2, 4]
    def __init__(self):
        return

    def test(self):
        for regex, word, answer in zip(self.regexs, self.words, self.answers):
            assert(reversedDFA(regex).find_max_pref(word[::-1]) == answer)