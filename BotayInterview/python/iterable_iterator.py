class Countdown:
    def __init__(self, start):
        self.start = start

    def __iter__(self):
        self.current = self.start
        return self

    def __next__(self):
        if self.current < 0:
            raise StopIteration
        else:
            v = self.current
            self.current -= 1
            return v

cd = Countdown(5)
for n in cd:
    print(n)

my_list = [1, 2, 3]

my_iter = iter(my_list)
print(next(my_iter))
print(next(my_iter))

print("for loop:")
it = iter(my_list)
while True:
    try:
        item = next(it)
        print(item)
    except StopIteration:
        break
print(iter(my_iter) is my_iter)
