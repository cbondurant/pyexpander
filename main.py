#!/usr/bin/python3

import pyexpander

def main():
    expr = "<word>"
    with open("test.bnf") as f:
        expander = pyexpander.Expander()
        expander.max_repeat = 3
        expander.parse_rules(f.readlines())
        print("Rules Defined: ", expander.defined_names['<word>'])
        for _ in range(5):
            print(*[expander.generate(expr) for _ in range(5)])

main()
