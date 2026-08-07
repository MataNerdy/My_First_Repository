try:
    with open("myfile.txt") as f:
        for t in f:
            print(t)
except Exception as e:
    print(e)

class DefenderVector:
    def __init__(self, v):
        self.__v = v

    def __enter__(self):
        self.__temp = self.__v[:]
        return self.__temp
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.__v[:] = self.__temp
        return False


v1 = [1, 2, 3]
v2 = [3, 4, 5]

try:
    with DefenderVector(v1) as dv:
        for i, a in enumerate(dv):
            print(dv)
            dv[i] += v2[i]
except:
    print("Error")
print(v1)