import logging
import logging.employee as employee

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('sample.log')
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

def add(x, y):
    return x + y

def substract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    try:
        result = x / y
    except ZeroDivisionError:
        logger.exception('Tried to divide by zero')
    else:
        return result

num_1 = 10
num_2 = 0

add_result = add(num_1, num_2)
logger.debug(f"Add: {num_1} + {num_2} = {add_result}".format(num_1, num_2, add_result))
sub_result = substract(num_1, num_2)
logger.debug("Substract: {} - {} = {}".format(num_1, num_2, sub_result))
multiply_result = multiply(num_1, num_2)
logger.debug("Multiply: {} * {} = {}".format(num_1, num_2, multiply_result))
divide_result = divide(num_1, num_2)
logger.debug("Divide: {} / {} = {}".format(num_1, num_2, divide_result))