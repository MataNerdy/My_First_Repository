from functools import lru_cache, singledispatch, wraps


class Circle:
    def __init__(self, radius):
        self.radius = radius

@property
def radius(self):
    return self._radius

@radius.setter
def radius(self, value):
    if value < 0:
        raise ValueError("Radius cannot be negative")
    self._radius = value

class StringUtils:
    @staticmethod
    def is_palindrome(s):
        s = s.lower()
        return s == s[::-1]

    @classmethod
    def from_string(cls, csv_string):
        parts = csv_string.split(",")
        return cls(*parts)

@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 0:
        raise ValueError("Negative arguments are not supported")
    if n in (0, 1):
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(10))

def debug(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args: {args}, kwargs: {kwargs}")
        return func(*args, **kwargs)
    return wrapper

@singledispatch
def serialize(obj):
    raise NotImplementedError(f"Cannot serialize object of type {type(obj)}")

@serialize.register
def _(obj: int):
    return f"INT:{obj}"

@serialize.register
def _(obj: list):
    return(f"List: {obj}")

print(serialize(42))
print(serialize([1, 2, 3]))
