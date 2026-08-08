import threading
import time

def fibonacci(n):
    if n<=1:
        return 1
    else:
        return fibonacci(n-1)+fibonacci(n-2)

def calculate_fibonacci(start, end, result):
    fib_seq = []
    for i in range(start, end):
        fib_seq.append(fibonacci(i))
    result.extend(fib_seq)

def main():
    num_terms = 30
    num_threads = 88
    chunk_size = num_terms // num_threads

    threads = []
    result = []

    start_time = time.time()

    for i in range(num_threads):
        start = i * chunk_size
        end = (i+1)*chunk_size if i != num_threads - 1 else num_terms
        thread = threading.Thread(target=calculate_fibonacci, args=(start, end, result))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    finish_time = time.time()
    print(result)
    print(finish_time-start_time)

if __name__ == "__main__":
    main()