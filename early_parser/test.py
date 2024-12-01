from unittest import TestCase
from early_parser import *


# Tests with 100% coverage
class ParserTest(TestCase):
    def test_check_parser(self):
        gram1 = Grammar()
        gram1.set_alphabet(["a", "b"])
        gram1.set_nonterminals(["S"])
        gram1.set_start("S")
        gram1.add_rule("S -> aSbS")
        gram1.add_rule("S ->")
        parser1 = Parser(gram1)
        self.assertTrue(parser1.check("aababb"))
        self.assertTrue(parser1.check("aaaabbbabb"))
        self.assertFalse(parser1.check("aaaabbb"))

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
        self.assertTrue(parser2.check("adc"))
        self.assertTrue(parser2.check("dddddabadadc"))
        self.assertFalse(parser2.check("caadddaaadddabadac"))
        self.assertFalse(parser2.check("dabdabdabdabda"))
