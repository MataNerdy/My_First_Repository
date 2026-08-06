class Key:
    def __init__(self, key):
        self.key = key

    def __hash__(self):
        return 1

    def __eq__(self, other):
        print(f"Comparing keys {self.key} and {other.key}")
        return self.key == other.key

d = {}
k1 = Key("A")
k2 = Key("B")
k3 = Key("A")

d[k1] = "Value for A"
d[k2] = "Value for B"

print(d[k3])
