import unittest
from DFA import reversedDFA

class Test(unittest.TestCase):
    def test(self):
        regexs = ['ab + c.aba. ∗ .bac. + . + ∗', 'acb..bab.c. ∗ .ab.ba. + . + ∗a.', '1 a +']
        words = ['babc', 'cbaa', 'bab']
        answers = [2, 4, 0]
        for regex, word, answer in zip(regexs, words, answers):
            assert(reversedDFA(regex).find_max_pref(word[::-1]) == answer)

    def test_bad_symbols(self):
        regexs = ['a k +', '1 2. 3. ']
        for regex in regexs:
            with self.assertRaisesRegex(ValueError, 'Bad symbol.'):
                reversedDFA(regex)

    def test_few_operators(self):
        regexs = ['ab + c.aba ∗ .bac. + . + ∗', 'ab + c']
        for regex in regexs:
            with self.assertRaisesRegex(ValueError, 'Bad input. Few operators.'):
                reversedDFA(regex)

    def test_bad_input(self):
        regexs = ['a ∗ + b ∗', '∗ ab. ∗ a', '.']
        for regex in regexs:
            with self.assertRaisesRegex(ValueError, 'Bad input. Few arguments.'):
                reversedDFA(regex)


if __name__ == "__main__":
    unittest.main()