"""
source: own
author: https://github.com/MarkShawn2020
create: Aug 15, 2022, 01:04
"""
from pydantic import conint, confloat


def strict_int(le: int):
    """
    cannot use strict for int, with np.int
    :param le:
    :return:
    """
    return conint(strict=False, ge=0, le=le)


def strict_float(le: float):
    return confloat(strict=True, ge=0, le=le)


def strict_percent():
    return strict_float(le=1)