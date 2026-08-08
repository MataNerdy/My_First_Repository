import time
from contextlib import contextmanager


class TemporaryValue:
    def __init__(self, obj, name, value):
        self.obj = obj
        self.name = name
        self.value = value

    def __enter__(self):
        self.old_value = getattr(self.obj, self.name)
        setattr(self.obj, self.name, self.value)
        return self
    def __exit__(self, e_t, e_v, tb):
        setattr(self.obj, self.name, self.old_value)

class Config:
    debug = False

class MyContext:
    def __enter__(self):
        print("Enter in Context")
        return 'hello'
    def __exit__(self, exc_type, exc_value, traceback):
        print("Exit from Context")
        print("Error type:", exc_type)
        print("Exception value:", exc_value)
        print("Traceback:", traceback)

class SupressZeroDivision:
    def __enter__(self):
        return self
    def __exit__(self, e_t, e_v, tb):
        if e_t == ZeroDivisionError:
            print("Division by Zero happend")
        return True

class Timer:
    def __enter__(self):
        self.start = time.time()
        return self
    def __exit__(self, e_t, e_v, tb):
        self.end = time.time()
        self.elapsed = self.end - self.start
        print(f"Время выполнения: {self.elapsed:.4f} секунд")

@contextmanager
def my_context():
    print("Вход")
    try:
        yield "hello"
    finally:
        print("Выход")

with my_context() as value:
    print(value)

with MyContext() as value:
    print(value)

with SupressZeroDivision():
    x = 1/0

with Timer():
    total = sum(range(1000000))

c = Config()

print(c.debug)

with TemporaryValue(c, "debug", True):
    print(c.debug)

print(c.debug)
