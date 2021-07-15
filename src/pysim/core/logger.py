import logging
from pysim.core.experiment import ex

logger = logging.getLogger('pysim')
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(levelname)s - %(name)s - %(message)s')

ch.setFormatter(formatter)

logger.addHandler(ch)

ex.logger = logger
