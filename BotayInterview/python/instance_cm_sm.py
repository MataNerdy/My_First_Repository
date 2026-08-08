class User:
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email
    def is_adult(self):
        return self.age >= 18
    @classmethod
    def from_birth_year(cls, name, birth_year, email):
        age = 2026-birth_year
        return cls(name=name, age=age, email=email)
    @staticmethod
    def normalize_email(email):
        return email.strip().lower()

class Admin(User):
    pass

class Price:
    @staticmethod
    def with_vat(amount: float, vat: float=0.2):
        return amount*(1+vat)

class Example:
    def instance_method(self):
        return "Works with object"
    @classmethod
    def class_method(cls):
        return "Works with class"
    @staticmethod
    def static_method():
        return "Not getings self or cls"

obj = Example()
print(obj.instance_method())
print(Example.class_method())
print(Example.static_method())

print(Price.with_vat(100))

u1 = User("Anna", 25, "anna@mail.ru")
u2 = User.from_birth_year("Nick", 1991, "nick@mail.ru")
u3 = Admin.from_birth_year("Roman", 2003, "admin@mail.ru")
email = User.normalize_email(' TEST@EXAMPLE.COM ')
print(email)
print(u1.is_adult())
print(u2.age)
print(u3.age, type(u3))