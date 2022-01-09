from sage.all import *


def ex4(p, q):
    x = randrange(q)
    y = randrange(q)

    X = Mod(q ** x, p)
    Y = Mod(q ** y, p)

    return Mod(X ** y, p) == Mod(Y ** x, p)
