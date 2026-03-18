import sys
from pprint import pprint
from pack_1.file_11 import a

pprint(sys.path)

print(a)

def func_2(n: int) -> int:
    return n + n

print(func_2(a))