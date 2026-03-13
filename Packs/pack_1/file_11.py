from .file_12 import num

print("Это модуль", __name__)

def some_func(n: int) -> float:
    return (n + n) / n**n

result = some_func(num)