import functools


class CountCalls:
    def __init__(self, func):
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        return self.func(*args, **kwargs)


@CountCalls
def say_hello():
    print("Hello!")

for i in range(4):
    say_hello()
    print(say_hello.count)



def log_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("Вызов {func.__name__} c {args=}, {kwargs=}")
        return func(*args, **kwargs)
    return wrapper

def retry(max_appemps):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_appemps):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == max_appemps - 1:
                        raise
            return None
        return wrapper
    return decorator

@log_calls
def add(a, b):
    """ Складывает два числа """
    return a+b

@retry(3)
def usability_api():
    pass

print(add(5, 3))
print(add.__name__)
print(add.__doc__)
