import sys


class Grammar:
    size_of_nt = 100
    size_of_gram = int()
    start_nt = str()
    rules = list()
    list_of_nt = list()
    alphabet = list()

    class Iterator:
        char_id = int()
        rule_id = int()
        rules = list()
        size_of_nt = 100

        def get_rule(self):
            return self.rules[self.char_id][self.rule_id]

        def is_valid(self):
            return self.size_of_nt > self.char_id >= 0 and \
                   0 <= self.rule_id < len(self.rules[self.char_id])

        def __init__(self, rules, c='!'):
            self.char_id = ord(c) - ord('!')
            self.rule_id = 0
            self.rules = rules

        def __iter__(self):
            return self

        def __next__(self):
            self.rule_id += 1
            if self.rule_id >= len(self.rules[self.char_id]):
                self.rule_id = 0
                self.char_id += 1
                while self.char_id < self.size_of_nt and len(self.rules[self.char_id]) == 0:
                    self.char_id += 1
            if not self.is_valid():
                raise StopIteration
            return self.get_rule()

    def __init__(self, start: str = 'S'):
        self.start_nt = start
        self.size_of_gram = 0
        self._iter = self.__iter__

    def get_rule(self):
        return self.rules

    def get_non_terminals(self):
        return self.list_of_nt

    def get_terminals(self):
        return self.alphabet

    def set_start(self, strng):
        self.start_nt = strng

    def set_nonterminals(self, list_of_nt):
        self.list_of_nt = list_of_nt

    def set_alphabet(self, alphabet):
        self.alphabet = alphabet

    def rule_check(self, rule: str) -> list:
        rules = []
        cur_rule = ""
        flag = False
        for indx in range(3, len(rule)):
            if rule[indx] == ' ' or rule[indx] == '\n':
                continue
            elif rule[indx] not in self.list_of_nt and rule[indx] not in self.alphabet:
                flag = True
                break
            else:
                cur_rule += rule[indx]
        if flag:
            print("Nonvalid symbol")
            sys.exit()
        rules.append([rule[0], cur_rule])
        return rules

    def is_non_terminal(self, c: str) -> bool:
        return c in self.list_of_nt

    def is_valid_rule(self, rule: str) -> bool:
        valid = (len(rule) >= 3 and self.is_non_terminal(rule[0]) and rule[1] == '-' and rule[2] == '>')
        if not valid:
            return False
        self.rule_check(rule)
        return True

    def add_rule(self, rule: str) -> bool:
        rule = rule.replace(" ", '')
        if self.is_valid_rule(rule):
            rules_pack = self.rule_check(rule)
            for single_rule in rules_pack:
                self.rules.append(single_rule)
                self.size_of_gram += 1
            return True
        return False

    def __iter__(self):
        self._iter = self.Iterator(self.rules)
        return self._iter.__iter__()
