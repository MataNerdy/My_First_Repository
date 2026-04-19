import logging
import sys

format_1 = '#%(levelname)-8s [%(asctime)s] - %(filename)s:'\
            '%(lineno)d - %(name)s - %(message)s'

format_2 = '[{asctime}] #{levelname:8} {filename}:'\
            '{lineno} - {name} - {message}'

formatter_1 = logging.Formatter(fmt=format_1)
formatter_2 = logging.Formatter(fmt=format_2, style='{')

logger = logging.getLogger(__name__)
stderr_handler = logging.StreamHandler()
stdout_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler('logs.log')

stderr_handler.setFormatter(formatter_1)
stdout_handler.setFormatter(formatter_2)
file_handler.setFormatter(formatter_1)

logger.addHandler(stdout_handler)
logger.addHandler(file_handler)
logger.addHandler(stderr_handler)

print(logger.handlers)

logger.warning("Предупреждение")