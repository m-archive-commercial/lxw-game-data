"""
source: own
author: https://github.com/MarkShawn2020
create: Aug 15, 2022, 01:04
"""
from pydantic import conint, confloat


def strict_int(le: int, **kwargs):
    """
    cannot use strict for int, with np.int
    :param le:
    :return:
    """
    return conint(strict=False, ge=0, le=le, **kwargs)


def strict_float(le: float, **kwargs):
    return confloat(strict=True, ge=0, le=le, **kwargs)


def strict_percent(**kwargs):
    return strict_float(le=1, **kwargs)