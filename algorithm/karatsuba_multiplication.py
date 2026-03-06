def karatsuba(x, y):
    if x < 10 or y < 10:
        return x * y

    n = max(len(str(x)), len(str(y)))
    m = n // 2

    a = x // 10**m
    b = x % 10**m
    c = y // 10**m
    d = y % 10**m

    p = a + b
    q = c + d
    ac = karatsuba(a, c)
    bd = karatsuba(b, d)
    pq = karatsuba(p, q)

    abcd = pq - ac - bd

    return ac * 10 ** (2 * m) + abcd * 10 ** m + bd

print(karatsuba(1234, 5678))

X = 31415926535897932384626433832795028841
Y = 27182818284590452353602874713526624977
print(karatsuba(X, Y) == X * Y)