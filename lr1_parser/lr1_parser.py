from grammar import *


class Parser:
    gramm = None
    table = []

    def __init__(self, gram: Grammar = Grammar()):
            self.gramm = gram

    def dotattach(self, prod):
        LHS, RHS = prod
        return [LHS, '.' + RHS]

    def dotsym(self, item):
        LHS, RHS = item
        if RHS.endswith('.'):
            return ''
        return RHS.split('.')[1][0]

    def rmdot(self, item):
        LHSi, RHSi = item
        return [LHSi, RHSi.replace('.', '')]

    def dotprogress(self, item):
        LHSi, RHSi = item
        ls = list(RHSi)
        i = ls.index('.')
        ls[i], ls[i + 1] = ls[i + 1], ls[i]
        return [LHSi, ''.join(ls)]

    def makeitems(self):
        nterminals = set(self.gramm.get_non_terminals())
        terminals = set(self.gramm.get_terminals())

        def inner(I):
            J = list(I)
            done = False
            while not done:
                done = True
                for item in J:
                    B = self.dotsym(item)
                    if B not in nterminals:
                        continue
                    for prod in self.gramm.get_rule():
                        LHS, RHS = prod
                        if LHS != B:
                            continue
                        new_item = self.dotattach(prod)
                        if new_item in J:
                            continue
                        J.append(list(new_item))
                        done = False
            return J

        def goto(I, X):
            J = []
            for item in I:
                B = self.dotsym(item)
                if B == X:
                    new_item = self.dotprogress(item)
                    J.append(list(new_item))
            return J

        def items():
            C = [inner([self.dotattach(self.gramm.get_rule()[0])])]
            S = list(nterminals.union(terminals))
            goto_moves = {}
            done = False
            while not done:
                done = True
                for index, I in enumerate(C):
                    goto_moves[index] = [None] * len(S)
                    for sym in S:
                        J = inner(goto(I, sym))
                        if len(J) == 0:
                            continue
                        if J not in C:
                            C.append(J)
                            done = False
                        goto_moves[index][S.index(sym)] = C.index(J)

            return C, S, goto_moves

        return items

    def getfnf(self):
        fsym = self.gramm.get_rule()[0][0]
        fcache, scache = {}, {}
        nterminals = set(self.gramm.get_non_terminals())
        terminals = set(self.gramm.get_terminals())

        def first(X):
            if X in fcache:
                return fcache[X]
            res = set()
            Xp = [P for P in self.gramm.get_rule() if P[0] == X]
            for prod in Xp:
                LHS, RHS = prod
                for index, sym in enumerate(RHS):
                    if sym == X:
                        break
                    if sym in terminals.union(''):
                        res = res.union(sym)
                        break
                    fy = first(sym)
                    res = res.union(fy - {''})
                    if '' not in fy:
                        break
                    if index == len(RHS) - 1:
                        res = res.union({''})
            fcache[X] = res
            return fcache[X]

        def fof(b):
            res = set()
            for index, sym in enumerate(b):
                if sym in terminals.union({''}):
                    res = res.union({sym})
                    break
                fy = first(sym)
                res = res.union(fy - {''})
                if '' not in fy:
                    break
                if index == len(b) - 1:
                    res = res.union({''})
            return res

        def follow(X):
            if X in scache:
                return scache[X]
            res = set()
            if X == fsym:
                res = res.union({'$'})
            Xp = [P for P in self.gramm.get_rule()
                  if X in P[1]]
            for prod in Xp:
                LHS, RHS = prod
                for index, sym in enumerate(RHS):
                    if sym != X:
                        continue
                    if (index == len(RHS) - 1) and (LHS != sym):
                        res = res.union(follow(LHS))
                        continue
                    fb = fof(RHS[index + 1:])
                    res = res.union(fb - {''})
                    if ('' in fb) and (LHS != sym):
                        res = res.union(follow(LHS))

            scache[X] = res
            return scache[X]

        return first, follow

    def construct(self):
        items = self.makeitems()
        first, follow = self.getfnf()
        states, syms, T = items()
        syms.append('$')
        self.table = [dict() for i in states]
        nterminals = self.gramm.get_non_terminals()
        terminals = self.gramm.get_terminals()

        for i in range(len(states)):
            for j in range(len(syms) - 1):
                sym = syms[j]
                if T[i][j] == None:
                    continue
                if sym in nterminals:
                    self.table[i][sym] = ["goto", T[i][j]]
                else:
                    self.table[i][sym] = ["shift", T[i][j]]

        for index, I in enumerate(states):
            for item in I:
                B = self.dotsym(item)
                if B != '':
                    continue
                LHSi, RHSi = item
                pidx = self.gramm.get_rule().index(self.rmdot(item))
                if pidx == 0:
                    self.table[index]['$'] = ["accept", index]
                    break
                foleft = follow(LHSi)
                for sym in foleft:
                    if sym in self.table[index]:
                        raise Exception("Conflict in state-sym.")
                    self.table[index][sym] = ["reduce", pidx]

    def predict(self, string) -> bool:
        index = 0
        sstack = [0]
        symstack = []
        actionstr = ""
        buf = list(string + '$')
        self.construct()

        while True:
            sym = buf[index]
            s = sstack[-1]

            if sym not in self.table[s]:
                print(actionstr)
                return False
            action, value = self.table[s][sym]

            if action == "shift":
                symstack.append(sym)
                sstack.append(value)
                index += 1

            if action == "reduce":
                LHS, RHS = self.gramm.get_rule()[value]
                for i in range(len(RHS)):
                    sstack.pop()
                    symstack.pop()
                s = sstack[-1]
                sstack.append(self.table[s][LHS][1])
                symstack.append(LHS)

            if action == "accept":
                print(actionstr)
                return True
