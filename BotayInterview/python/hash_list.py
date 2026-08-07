print(list.__hash__)
# print(hash([1, 3, 5]))
key = [1, 2, 3]
# data = {key: "value"}
key.append(4)

class User:
    pass
user = User()
print(hash(user))
user.name = "Roman"
print(hash(user))

class User:
    def __init__(self, name=None):
        self.name = name
    def __hash__(self):
        return hash(self.name)

user1 = User("Bob")
print("1:", hash(user1))
user2 = User("Bob")
print("2:", hash(user2))
print(user1 == user2)
user = User()
user.name = "Alice"
print("3:", hash(user))

class HashableList(list):
    def __hash__(self):
        return 42

one = HashableList([1])
two = HashableList([2])
data = {
    one: "value1",
    two: "value2",
    }
print(one == two)
one[0] = 2
print(one == two)

print(hash((1, 3,5)))
# print(hash((1, [2, 3])))