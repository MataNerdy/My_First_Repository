import logging

class ErrorLogFilter(logging.Filter):
    def filter(self, record):
        return record.levelname == "ERROR" and "важно" in record.msg.lower()

logger = logging.getLogger(__name__)
stderr_handler = logging.StreamHandler()
stderr_handler.addFilter(ErrorLogFilter())
logger.addHandler(stderr_handler)

logger.error("Важно! Это лог с ошибкой!")
logger.warning("Важно! Это лог с предупреждением!")
logger.error("Это просто лог с ошибкой!")
logger.info("Важно! Это лог с информацией!")