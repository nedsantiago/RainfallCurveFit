import logging
from logging.config import fileConfig


fileConfig(r"../src/logging.conf")
logger = logging.getLogger(__name__)