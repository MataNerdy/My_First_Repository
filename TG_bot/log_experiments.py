import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.level = logging.DEBUG

logger.warning("Предупреждение")
logger.debug("Отладочная информация")

logging.basicConfig()

logging.debug("Это лог debug")
logging.info('Это лог info')
logging.warning('Это лог warning')
logging.error("Это лог error")
logging.critical("Это лог critical")

print(logging.DEBUG)
print(logging.INFO)
print(logging.WARNING)
print(logging.ERROR)
print(logging.CRITICAL)

logger = logging.getLogger()
print(logger)
print(logger.parent)

logger = logging.getLogger(__name__)
print(logger.parent)

logger_1 = logging.getLogger('one.two')
print(logger_1.parent)

logger_2 = logging.getLogger('one.two.three')
print(logger_2.parent)
