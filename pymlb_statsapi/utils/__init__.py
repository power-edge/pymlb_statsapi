"""
created by nikos at 5/2/21
"""
import datetime
import os
from functools import reduce


from importlib import resources

CONFIGS_PATH = "%s/configs" % reduce(
    lambda d, _: os.path.dirname(d),
    range(4),
    os.path.realpath(__file__)
)
