import sys
import timeit

a = [1, 2, 3]
print(sys.getsizeof(a))
print(timeit.timeit(lambda: [1, 2, 3]))
b = (1, 2, 3)
print(sys.getsizeof(b))
print(timeit.timeit(lambda: (1, 2, 3)))
a.append(4)
print(a)
try:
    b.append(4)
except AttributeError as e:
    print(f"Error: {e}")

try:
    d1 = {a: "list"}
    print(d1)
except TypeError as e:
    print(f"Error: {e}")

d2 = {b: "tuple"}
print(d2)

t = (1, 2, [3, 4])
t[2].append(5)
print(t)