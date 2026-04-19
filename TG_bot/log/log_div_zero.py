import logging

logger = logging.getLogger(__name__)

try:
    print(4/2)
    print(4/0)
except ZeroDivisionError:
    logger.error("Тут было исключение")