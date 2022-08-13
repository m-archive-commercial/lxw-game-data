"""
source: own
author: https://github.com/MarkShawn2020
create: Aug 13, 2022, 23:23
"""
from typing import Type

from pydantic import ConstrainedFloat

$END


class StatFloat(ConstrainedFloat):
    stat_mean: float
    stat_ge: float
    stat_le: float


def statfloat(
    *,
    strict: bool = False,
    gt: float = None,
    ge: float = None,
    lt: float = None,
    le: float = None,
    multiple_of: float = None,
    stat_mean: float = None,
    stat_ge: float = None,
    stat_le: float = None
) -> Type[float]:
    # use kwargs then define conf in a dict to aid with IDE type hinting
    namespace = dict(strict=strict, gt=gt, ge=ge, lt=lt, le=le, multiple_of=multiple_of, stat_mean=stat_mean,
        stat_ge=stat_ge, stat_le=stat_le)
    return type('StatFloatValue', (StatFloat,), namespace)