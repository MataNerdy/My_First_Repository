class EvenNumbers:
    def __init__(self, max):
        self.max = max
        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current > self.max:
            raise StopIteration
        else:
            v = self.current
            self.current += 2
            return v

class EvenRange:
    def __init__(self, max):
        self.max = max

    def __iter__(self):
        return EvenNumbers(self.max)

evens = EvenNumbers(10)
print(list(evens))
print(list(evens))

r = EvenRange(10)
print(list(r))
print(list(r))