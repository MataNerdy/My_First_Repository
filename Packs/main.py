from pack_1 import file_11
from pack_2.pack_21 import file_211

print("Это основной модуль main.py, его имя в процессе выполнения:", __name__)

print("Значение переменной a из модуля file_11:", file_11.a)
print("Значение переменной b из модуля file_211:", file_211.b)
print("Значение словаря some_dict из модуля file_211:", file_211.some_dict)