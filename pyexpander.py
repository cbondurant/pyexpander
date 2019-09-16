import string
from random import choice

import generators

class ParseError(Exception):
    pass

class Expander:


    SINGLE_LEXEMES = ["=","*", "+", "|"]

    def __init__(self, rules = None):
        self.defined_names = {}
        self.max_repeat = 10

        if type(rules) == str:
            self.parse(rules.split("\n"))
        elif type(rules) == list:
            self.parse(rules)

    def seek(self, iterator, target):
        subchar = ""
        subtoken = ""
        try:
            while subchar != target:
                subchar = next(iterator)
                subtoken += subchar
            return subtoken
        except StopIteration:
            raise ParseError("End of expression reached while looking for {}.".format(target))

    def is_name(self, term):
        return term[0] == "<" and term[-1] == ">"

    # lexes a single-line expression into accepted tokens
    def lex(self, expr):
        lexemes = []
        expr_iter = iter(expr)
        for char in expr_iter:
            # TODO: Better bracket matching
            if char == "<":
                lexemes.append("<" + self.seek(expr_iter, ">"))
            elif char == "\'":
                lexemes.append("\'" + self.seek(expr_iter, "\'"))
            elif char == "\"":
                lexemes.append("\"" + self.seek(expr_iter, "\""))
            elif char == "(":
                lexemes.append("(" + self.seek(expr_iter, ")"))
            elif char == "[":
                lexemes.append("[" + self.seek(expr_iter, "]"))
            elif char in self.SINGLE_LEXEMES:
                lexemes.append(char)
            elif char == "#":
                return lexemes
            elif char in string.whitespace:
                continue
            else:
                raise ParseError("Invalid char in expr {}: {}".format(expr, char))
        return lexemes

    def parse_rules(self, rules):
        rules = [self.lex(rule) for rule in rules]
        for rule in rules:
            self.parse_rule(rule)

    def parse_rule(self, rule):
        if len(rule):
            if not self.is_name(rule[0]):
                raise ParseError("Error in rule {}: {} is not a valid name.".format(rule, rule[0]))
            if not rule[1] == "=":
                raise ParseError("Error in rule {}: More than one name being assigned.".format(rule))
            if rule[0] in rule[2:]:
                raise ParseError("Error in rule {}: Recursive definition".format(rule))
            self.defined_names[rule[0]] = self.parse_expr(rule[2:])

    def parse_expr(self, expr):
    # converts expression into a tree of functions to be called
        tokens = []
        iexpr = iter(expr)
        for term in iexpr:
            if term in generators.NAME_GENERATORS:
                tokens.append(generators.NAME_GENERATORS[term])
            elif term in self.defined_names:
                tokens.append(self.defined_names[term])
            elif term == "|":
                choices = [generators.concat(*tokens)]
                choice = []
                for subterm in iexpr:
                    if subterm == "|":
                        if not choice:
                            raise ParseError("Empty choices in expressions not allowed: {}".format(expr))
                        choices.append(self.parse_expr(choice))
                        choice = []
                    else:
                        choice.append(subterm)
                choices.append(self.parse_expr(choice))
                return generators.choose(*choices)

            elif term == "*":
                tokens[-1] = generators.repeater(tokens[-1], self.max_repeat)
            elif term == "+":
                tokens[-1] = generators.repeater(tokens[-1], self.max_repeat, 1)
            elif term[0] == "\"" or term[0] == "'":
                tokens.append(generators.literal(term[1:-1]))
            elif term[0] == "(":
                lexterm = self.lex(term[1:-1])
                tokens.append(self.parse_expr(lexterm))
            elif term[0] == "[":
                lexterm = self.lex(term[1:-1])
                tokens.append(generators.optional(self.parse_expr(lexterm)))
            else:
                raise ParseError("Unknown name: {}".format(term))

        return generators.concat(*tokens)

    def generate(self, expr):
        expr = self.lex(expr)
        return self.parse_expr(expr)()
