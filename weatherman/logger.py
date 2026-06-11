import logging
import sys


logging.basicConfig(format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)], level=logging.INFO)
logger = logging.getLogger(__name__)
