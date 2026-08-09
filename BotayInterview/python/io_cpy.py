import time
import requests
import math
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def cpu_heavy_task(n):
    primes = []
    for num in range(2, n):
        is_prime = True
        for i in range(2, int(math.sqrt(n))+1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
    return len(primes)

def io_heavy_task(url):
    try:
        responce = requests.get(url, timeout=5)
        return len(responce.content)
    except requests.exceptions.RequestException:
        return 0

if __name__=="__main__":
    start = time.time()
    result_cpu = cpu_heavy_task(10000)
    print(f"CPU-bound (один вызов): {result_cpu} простых чисел, время: {time.time() - start:.2f} сек")
    urls = ["https://httpbin.org/delay/1"] * 5

    start = time.time()
    for url in urls:
        io_heavy_task(url)
    print(f"I/O-bound (последовательно): время: {time.time() - start:.2f} сек")

    start = time.time()
    with ThreadPoolExecutor() as executor:
        list(executor.map(io_heavy_task, urls))
    print(f"I/O-bound (через ThreadPool): время: {time.time() - start:.2f} сек")

    numbers = [5000, 6000, 7000, 8000]
    start = time.time()
    with ProcessPoolExecutor() as executor:
        list(executor.map(cpu_heavy_task, numbers))
    print(f"CPU-bound (через ProcessPool): время: {time.time() - start:.2f} сек")