__all__ = ['some_var', 'yet_some_var', 'another_func']

print("Это модуль", __name__)

some_var: int  = 42
another_var: int = 242
yet_some_var: str = 'some_text'

def _reverse_text(text: str) -> str:
    return text[::-1]

def some_func(text: str, times: int) -> str:
    return _reverse_text(text * times)

def another_func() -> None:
    pass
