import copy

config = {
    "model": {
        "name": "resnet",
        "params": {
            "lr": 0.001
        }
    }
}
new_config = copy.deepcopy(config)
new_config["model"]["params"]["lr"] = 0.0001
print(config["model"]["params"]["lr"])
print(new_config["model"]["params"]["lr"])

x = 10
print(x)
y = x
z = copy.copy(x)
t = copy.deepcopy(x)
print(x is y)
print(x is z)
print(x is t)


a = [1, 3, 5]
print(a)
b = a
b[0] = 2
print(f"{a=}, {b=}")
c = copy.copy(a)
c[1] = 4
print(f"{a=}, {c=}")
d = copy.deepcopy(a)
d[2] = 6
print(f"{a=}, {d=}")
print(a is b)
print(a is c)
print(a is d)

a = [[1, 2], [3, 4]]
print(a)
b = a
print(a is b)
a[0].append(5)
print(a)
print(b)

a = [[1, 2], [3, 4]]
b = copy.copy(a)
print(a is b)
print(a[0] is b[0])
a[0].append(5)
b.append([6, 7])
print(a)
print(b)

a = [[1, 2], [3, 4]]
b = copy.deepcopy(a)
print(a is b)
print(a[0] is b[0])
a[0].append(5)
b.append([6, 7])
print(a)
print(b)