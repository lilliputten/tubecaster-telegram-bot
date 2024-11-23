import logging

# @see https://habr.com/ru/companies/wunderfund/articles/683880/
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
    #  filename="py_log.log", filemode="w",
)
logger = logging.getLogger('api/index')

# Module exports...
__all__ = [
    'logger',
]
