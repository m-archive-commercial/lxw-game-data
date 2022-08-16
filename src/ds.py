"""
source: own
author: https://github.com/MarkShawn2020
create: Aug 15, 2022, 01:02
notes:
    1. keep in mind that we should put `int` in the Enum Base,
        so that it can export the valid int value,
        especially when dumping into a csv file in Pandas.
"""
from enum import Enum


class ExtendedEnum(Enum):
    """
    ref: https://stackoverflow.com/a/54919285/9422455
    """

    @classmethod
    def values(cls):
        return list(map(lambda i: i.value, cls))


class FeatDifficultyLevel(int, ExtendedEnum):
    EASY = 0
    MID = 1
    HARD = 2


class FeatGiftType(int, ExtendedEnum):
    NONE = 0
    GOOD = 1
    BAD = -1


class FeatRealScore(int, ExtendedEnum):
    NO_DATA = -1
    DATA_SAME = 0
    DATA_DIFF = 1
