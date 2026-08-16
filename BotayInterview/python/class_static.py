import math


class MathUtils:
    @staticmethod
    def euclidian_distance(p1: tuple[float, ...], p2: tuple[float, ...]) -> float:
        if len(p1) != len(p2):
            raise ValueError("Точки должны иметь одинаковую размерность")
        squared_sum = sum((a - b) ** 2 for a, b in zip(p1, p2))
        return math.sqrt(squared_sum)

    @staticmethod
    def manhattan_distance(p1: tuple[float, ...], p2: tuple[float, ...]) -> float:
        if len(p1) != len(p2):
            raise ValueError("Точки должны иметь одинаковую размерность")
        return sum(abs(a - b) for a, b in zip(p1, p2))

class Date:
    def __init__(self, day: int, month: int, year: int):
        self.day = day
        self.month = month
        self.year = year

    @classmethod
    def from_string(cls, date: str) -> 'Date':
        d, m, y = map(int, date.split('-'))
        return cls(d, m, y)

    @classmethod
    def from_dict(cls, data: dict) -> 'Date':
        return cls(data["day"], data["month"], data["year"])

date1 = Date(25, 12, 2025)
date2 = Date.from_string("25-12-2025")
dat33 = Date.from_dict({"day": 25, "month": 12, "year": 2023})
