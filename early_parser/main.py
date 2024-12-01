import early_parser

tmp = input().split(" ")
N = int(tmp[0])
E = int(tmp[1])
P = int(tmp[2])

gram = early_parser.Grammar()

gram.set_nonterminals(list(input()))

gram.set_alphabet(list(input()))

for _ in range(P):
    gram.add_rule(input())

parser = early_parser.Parser(gram)

gram.set_start(input())

M = int(input())

for _ in range(M):
    tmp = input()
    if parser.check(tmp):
        print("Yes")
    else:
        print("No")
