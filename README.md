# Pyexpander
A tool for generating valid context-free language examples

## Usage
Currently this tool is a very simple library with an example driver. `.bnf` files can be imported by an `Expander` object and then queries can be made using more bnf expressions, either in the form of single names, or more complex expressions.

## implemented notation:

- Notation is mostly equivlent to EBNF notation
- Parenthesis can be used to create an order of operations.
- Quotations are used for all string literals, however escaping is not currently implemented
- Names are quoted with `<>` pairs
- Optional strings are defined by `[]` pairs
- Comments can be made with `#`, all text after a `#` are considered comments and not processed
- Repetition can be done with `*`(Zero or more times) and `+`(One or more times)
- Choice between two or more options are divided by `|`
