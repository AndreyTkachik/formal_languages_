from grammar import *


class Parser:
    gramm = None
    levels = []

    def __init__(self, gram: Grammar = Grammar()):
        self.gramm = gram

    class Situation:
        rule = str()
        position_in_rule = int()
        position_in_word = int()

        def __init__(self, rule: str, position_in_rule: int, position_in_word: int):
            self.rule = rule
            self.position_in_rule = position_in_rule
            self.position_in_word = position_in_word

        def __eq__(self, other):
            return (self.rule == other.rule and self.position_in_rule == other.position_in_rule \
                    and self.position_in_word == other.position_in_word)

        def __hash__(self):
            p = 13
            hash_ = self.position_in_word
            hash_ += (self.position_in_rule * (p ** 2)) % 13379696228
            k = 1
            for i in self.rule:
                hash_ += ord(i) * (p ** (2 + k))
                k += 1
            return hash_

    def scan(self, indx: int, letter: str):
        changed = False
        for situation in self.levels[indx]:
            tmp = False
            if (len(situation.rule) > situation.position_in_rule and
                    situation.rule[situation.position_in_rule]
                    == letter[indx]):
                state_previous_size = len(self.levels[indx + 1])
                self.levels[indx + 1].add(self.Situation(situation.rule, situation.position_in_rule + 1, \
                                                         situation.position_in_word))
                tmp = (len(self.levels[indx + 1]) != state_previous_size)
            changed |= tmp
        return changed

    def predict(self, indx: int) -> bool:
        changed = False
        situations = [i for i in self.levels[indx]]
        for situation in situations:
            tmp = False
            if situation.position_in_rule < len(situation.rule):
                if self.gramm.is_non_terminal(situation.rule[situation.position_in_rule]):
                    non_term = situation.rule[situation.position_in_rule]
                    new_states = [self.Situation(rl, 3, indx) for rl in self.gramm if rl[0] == non_term]
                    rules_in_situation = len(self.levels[indx])
                    for state in new_states:
                        self.levels[indx].add(state)
                    tmp = (len(self.levels[indx]) != rules_in_situation)
            changed |= tmp
        return changed

    def complete(self, indx: int) -> bool:
        changed = False
        situations = [i for i in self.levels[indx]]
        for situation in situations:
            tmp = False
            if situation.position_in_rule == len(situation.rule):
                non_terminal = situation.rule[0]
                lvl = situation.position_in_word
                new_states = []
                for prev_it in self.levels[lvl]:
                    if (prev_it.position_in_rule < len(prev_it.rule) and prev_it.rule[prev_it.position_in_rule] \
                            == non_terminal):
                        new_states.append(self.Situation(prev_it.rule, prev_it.position_in_rule + 1,
                                                         prev_it.position_in_word))
                prev_sz = len(self.levels[indx])
                for new_state in new_states:
                    self.levels[indx].add(new_state)
                tmp = (len(self.levels[indx]) != prev_sz)
            changed |= tmp
        return changed

    def check(self, word: str) -> bool:
        self.levels = [set() for _ in range(len(word) + 1)]
        self.levels[0].add(self.Situation('#->S', 3, 0))
        changed = True
        while changed:
            changed = self.complete(0)
            changed |= self.predict(0)
        for indx in range(len(word)):
            self.scan(indx, word)
            changed = True
            while changed:
                changed = self.complete(indx + 1)
                changed |= self.predict(indx + 1)
        result = self.Situation('#->S', 4, 0)
        for situation in self.levels[len(word)]:
            if situation == result:
                return True
        return False
