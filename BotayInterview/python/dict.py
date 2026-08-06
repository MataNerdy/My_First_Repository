d = {"a": 1, "b": 2, "c": 3}

class BadKey:
    def __init__(self, key):
        self.key = key

    def __hash__(self):
        return 1

    def __eq__(self, other):
        print(f"Comparing keys {self.key} and {other.key}")
        return self.key == other.key

d = {BadKey("a"): 1, BadKey("b"): 2, BadKey("c"): 1}

print(d[BadKey("a")])
print(d[BadKey("b")])
print(d[BadKey("c")])