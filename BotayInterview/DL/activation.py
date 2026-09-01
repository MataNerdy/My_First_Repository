import math
import random
import timeit


def relu(x):
    if x < 0:
        return 0
    return x


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def tanh_manual(x):
    return (
        math.exp(x) - math.exp(-x)
    ) / (
        math.exp(x) + math.exp(-x)
    )


values = [random.uniform(-5, 5) for _ in range(500_000)]


for func in [relu, sigmoid, tanh_manual]:
    times = timeit.repeat(
        lambda f=func: [f(x) for x in values],
        repeat=5,
        number=1,
    )

    print(f"{func.__name__:12}: {min(times):.4f} s")