class User:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
    def __str__(self) -> str:
        return f"User {self.name}, {self.age} years old"
    def __repr__(self) -> str:
            return f"User(name={self.name!r}, age={self.age!r})"
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, User):
            return NotImplemented
        return (self.name == other.name) and (self.age == other.age)
    def __hash__(self) -> int:
            return hash((self.name, self.age))

class Batch:
    def __init__(self, items: list[str]):
        self.items = items
    def __len__(self) -> int:
        return len(self.items)
    def __getitem__(self, index: int) -> str:
        return self.items[index]

class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    def __add__(self, other) -> "Vector":
        return Vector(self.x+other.x, self.y+other.y)
    def __repr__(self) -> str:
        return f"Vector(x={self.x!r}, y={self.y!r})"

class Countdown:
    def __init__(self, start: int):
        self.current = start
    def __iter__(self):
        return self
    def __next__(self) -> int:
        if self.current <= 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value

class ManagedResource:
    def __enter__(self):
        print("open")
        return self
    def __exit__(self, e_t, e_v, tb):
        print("close")

class Multiplier:
    def __init__(self, factor: int):
        self.factor = factor
    def __call__(self, value: int):
        return self.factor * value

class Cart:
    def __init__(self, items: list[str]):
        self.items = items
    def __bool__(self) -> bool:
        return bool(self.items)

class Cart2:
    def __init__(self, items: list[str]):
        self.items = items
    def __len__(self) -> int:
        return len(self.items)

n = Cart([])
if n:
    print("+")
else:
    print("-")


n2 = Cart2([])
if n:
    print("+")
else:
    print("-")

x3 = Multiplier(3)
print(x3(5))

with ManagedResource() as r:
    print("work")

for x in Countdown(5):
    print(x)

v1 = Vector(3, 4)
v2 = Vector(2, 1)
print(v1+v2)


u1 = User("Anna", 25)
u2 = User("Anna", 25)
u3 = User("Anna", 24)
print(repr(u1))
print(str(u1))
print(u1 == u2)
print(u1 == u3)
print(u1 == v1)

btch = Batch(['a', 'b', 'c'])
print(len(btch))
print(btch[0])