import threading
import time

def write_to_file(file_path, start, end):
  for i in range(start, end):
    with open(file_path, 'a') as file:
      file.write(f"Line {i}\n")


def main():
    file_path = "output.txt"
    num_lines = 10000
    num_threads = 128

    chunk_size = num_lines // num_threads

    threads = []

    start_time = time.time()

    for i in range(num_threads):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size if i != num_threads - 1 else num_lines
        thread = threading.Thread(target=write_to_file, args=(file_path, start, end))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    finish_time = time.time()
    print("done")
    print(finish_time-start_time)

if __name__ == "__main__":
    main()