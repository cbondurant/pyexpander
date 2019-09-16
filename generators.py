import string
from random import randint, random, choice

class repeater:

    def __init__(self, item, max_count, min_count = 0):
        self.item = item 
        self.max_count = max_count
        self.min_count = min_count

    def __call__(self):
        result = ""
        for _ in range(randint(self.min_count, self.max_count)):
            result += self.item()
        return result

    def __str__(self):
        return "Repeater({},{},{})".format(self.min_count, self.max_count, str(self.item))

class literal:

    def __init__(self, item):
        self.item = item

    def __call__(self):
        return self.item

    def __str__(self):
        return "literal({})".format(str(self.item))

class concat:

    def __init__(self, *items):
        self.items = items

    def __call__(self):
        return "".join([f() for f in self.items])

    def __str__(self):
        return "concat({})".format(", ".join([str(i) for i in self.items]))

class optional:

    def __init__(self, item, chance=0.5):
        self.item = item
        self.chance = chance

    def __call__(self):
        if random() > self.chance:
            return self.item()
        else:
            return ""
    
    def __str__(self):
        return "optional({})".format(str(self.item))

class choose:
    def __init__(self, *items):
        self.items = items

    def __call__(self):
        return choice(self.items)()

    def __str__(self):
        return "choose({})".format(", ".join([str(i) for i in self.items]))

def ascii_letter():
    return choice(string.ascii_letters)
def ascii_lowercase():
    return choice(string.ascii_lowercase)
def ascii_uppercase():
    return choice(string.ascii_uppercase)
def digit():
    return choice(string.digits)
def whitespace():
    return choice(string.whitespace)
def consonant():
    return choice("bcdfghjklmnpqrstvwxyz")
def vowel():
    return choice("aeiou")

NAME_GENERATORS = {"<ascii letter>":ascii_letter,
                   "<ascii lowercase>":ascii_lowercase,
                   "<ascii uppercase>":ascii_uppercase,
                   "<digit>":digit,
                   "<whitespace>":whitespace,
                   "<consonant>":consonant,
                   "<vowel>":vowel}
