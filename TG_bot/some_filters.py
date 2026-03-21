some_list = [7, 14, 28, 32, 32, '56']

def custom_filter(list) -> bool:
    sum = 0
    for i in list:
        if isinstance(i, int) and i % 7 == 0:
            sum += i
    return sum <= 83

print(custom_filter(some_list))

def anonymous_filter(x)  -> bool:
    return (isinstance(x, str) and x.lower().count('я') >= 23)

print(anonymous_filter('Я - последняя буква в алфавите!'))
print(anonymous_filter('яяяяяяяяяяяяяяяяяяяяяяяя, яяяяяяяяяяяяяяяя и яяяяяяяя тоже!'))