"""
source: own
author: https://github.com/MarkShawn2020
create: Aug 15, 2022, 01:02
"""
from enum import Enum


class ExtendedEnum(Enum):
    """
    ref: https://stackoverflow.com/a/54919285/9422455
    """

    @classmethod
    def values(cls):
        return list(map(lambda i: i.value, cls))


class FeatDifficultyLevel(ExtendedEnum):
    EASY = 0
    MID = 1
    HARD = 2


class FeatGiftType(ExtendedEnum):
    GOOD = 0
    BAD = 1
    NONE = 2


class FeatRealScore(ExtendedEnum):
    NO_DATA = -1
    DATA_SAME = 0
    DATA_DIFF = 1