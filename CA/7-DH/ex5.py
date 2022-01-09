p = 1373
g = 2
X = 974

for x in range(p):
    if g ** x % p == X:
        print(x)
        break
