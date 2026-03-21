class MyClass:
    def __init__(self) -> None:
        pass

    def __call__(self) -> str:
        return 'Hello, I am an instance of MyClass!'

my_class_1 = MyClass()
my_class_2 = MyClass()

print(my_class_1())
print(my_class_2())