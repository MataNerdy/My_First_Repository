import sys
import requests

def main() -> None:
    print("Welcome to the Interview Training Program!")
    print("Python:", sys.executable)
    print("Requests version:", requests.__version__)

if __name__ == "__main__":
    main()