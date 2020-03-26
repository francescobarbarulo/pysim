import logging

logger = logging.getLogger('pysim')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(levelname)s - %(name)s - %(message)s')

ch.setFormatter(formatter)

logger.addHandler(ch)


