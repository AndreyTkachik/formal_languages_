from unittest import TestCase
from lr1_parser import *


# Tests with 96% coverage
class ParserTest(TestCase):
    def test_check_parser(self):
        gram1 = Grammar()
        gram1.set_nonterminals(["S", "A", "B", "C", "D"])
        gram1.set_alphabet(["a", "b"])
        gram1.add_rule("S -> A")
        gram1.add_rule("A -> aA")
        gram1.add_rule("A -> bA")
        gram1.add_rule("A -> aB")
        gram1.add_rule("B -> bC")
        gram1.add_rule("C -> bD")
        gram1.add_rule("D ->")
        gram1.set_start("S")
        parser1 = Parser(gram1)
        self.assertTrue(parser1.predict("ababb"))
        self.assertFalse(parser1.predict("aaabbba"))

        gram2 = Grammar()
        gram2.set_alphabet(['a', 'b', 'c', 'd'])
        gram2.set_nonterminals(['S', 'A', 'B'])
        gram2.set_start('S')
        gram2.add_rule('S -> AS')
        gram2.add_rule('S -> Ac')
        gram2.add_rule('A -> BbA')
        gram2.add_rule('A -> Bd')
        gram2.add_rule('B ->')
        gram2.add_rule('B -> a')
        parser2 = Parser(gram2)
        with self.assertRaises(Exception):
            parser2.predict("ababb")
