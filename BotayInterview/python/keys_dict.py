class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __hash__(self):
        return hash((self.x, self.y))
    def __eq__(self, other):
            return ((self.x == other.x) and (self.y == other.y))

key = [1,2]
d = {key: "value"}
key.append(3)
print(d[1,2,3])