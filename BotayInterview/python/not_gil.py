import numpy as np
import threading
import time

def io_task():
    time.sleep(1)

def cpu_numpy():
    a = np.random.random((1000, 1000))
    b = np.random.random((1000, 1000))
    c = np.dot(a, b)

def cpu_python():
    total = 0
    for i in range(10**7):
        total += i * i

start = time.perf_counter()
for _ in range(10):
    io_task()
finish = time.perf_counter()
print(finish-start)

start = time.perf_counter()
for _ in range(10):
    cpu_numpy()
finish = time.perf_counter()
print(finish-start)

start = time.perf_counter()
for _ in range(10):
    cpu_python()
finish = time.perf_counter()
print(finish-start)
