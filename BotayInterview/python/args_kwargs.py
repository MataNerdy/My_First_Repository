def print_numbers(*args):
    print(args)

def total_sum(*nums):
    s = 0
    for x in nums:
        s+=x
    return s

def print_user(**kwargs):
    print(kwargs)

def create_user(**fields):
    name = fields.get('name')
    age = fields.get('age')
    return {'name': name, 'age': age}

def func(a, b, *args, **kwargs):
    print(a, b)
    print(args)
    print(kwargs)

def load(path, *args, batch_size=32, **kwargs):
    print(path)
    print(args)
    print(batch_size)
    print(kwargs)

def add(a, b, c):
    return a+b+c

def create_person(name, age):
    return {"name": name, "age": age}

def log_call(func):
    def wrapper(*args, **kwargs):
        print("Function called")
        return func(*args, **kwargs)
    return wrapper

def connect(host, *post, **options):
    timeout = options.get('timeout', 10)
    retries = options.get('retries', 3)
    print(host, post, timeout, retries)

connect('localhost', 5432, timeout=5, retries=2)

@log_call
def multiply(x, y):
    return x*y

print(multiply(2, 5))

values = [1, 2, 3]
print(add(*values))
person = {'name': "Paul", 'age': 27}
p = create_person(**person)
print(p)


load('data.csv', 'extra1', 'extra2', batch_size=64, lr=1e-4)

func(1, 1, 2, 3, 5, c=7, d=12)
print_numbers(1, 2, 3)
print(total_sum(1, 2, 3))
print(total_sum(10, 20, 30, 40))

print_user(name='Roman', age=23, city='London')
user = create_user(name="Anna", age=25)
print(user)