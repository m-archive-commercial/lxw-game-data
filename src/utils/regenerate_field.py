"""
source: own
author: https://github.com/MarkShawn2020
create: Aug 15, 2022, 01:05
"""
from typing import Callable

from utils.log import get_logger

logger = get_logger('utils-regenerate-field')


def regenerate(funcGenerate: Callable, funcValidator: Callable, tried=0,
               maxTries=5
               ):
    logger.debug(f'[#{tried}] generating')
    if tried >= maxTries:
        raise Exception(f'failed to generate a valid field')
    value = funcGenerate()
    try:
        funcValidator(value)
    except:
        return regenerate(funcGenerate, funcValidator, tried + 1, maxTries)
    else:
        return value
