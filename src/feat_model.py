"""
source: own
author: https://github.com/MarkShawn2020
create: Aug 13, 2022, 22:31
"""
from enum import Enum

from pydantic import BaseModel, conint, confloat, validator

from log import get_logger

logger = get_logger("FeatModel")


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


class FeatIsRealScore(ExtendedEnum):
    NO_DATA = -1
    DATA_SAME = 0
    DATA_DIFF = 1


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


class FeatModel(BaseModel):
    """
    todo:
        1. add help/description on each field
        2. add stat constraint
    """

    storyTime: strict_float(le=100)  # (5, 10, 30)
    tutorialTime: strict_float(le=100)  # (5, 18, 40)
    duration: bool  # 0. 中途退出，1. 坚持最后
    score: strict_float(le=200)  # (5, 40, 100)
    difficultyLevel: FeatDifficultyLevel
    replayTimes: bool  # 0. 不重玩 1. 重玩
    hitRate: strict_percent()
    badRate: strict_percent()
    mismatchRate: strict_percent()
    keepaway: strict_float(le=200)  # (5, 60, 100)
    feedback: strict_percent()
    goodRate: strict_percent()
    moveNum: strict_float(le=200)  # (5, 40, 100)
    clickRate: strict_float(le=3000)  # (100, 830, 2000)
    npcHitRate: strict_percent()
    getbackRate: strict_percent()
    isAcceptGift: bool
    giftType: FeatGiftType
    isUpload: bool
    isRealScore: FeatIsRealScore
    bugTimes: bool
    batteryTimes: strict_int(le=20)  # (0, 2, 5)
    filterLenTimes: strict_int(le=20)  # (0,2,5)
    signalTimes: strict_int(le=20)  # (0,2,5)
    impulseTimes: strict_int(le=20)  # (0, 2,5)
    morePolicy: bool
    lifetime: strict_int(le=(20 >> 1 + 1) * 60)  # max: 660

    @validator('lifetime')
    def validate_lifetime(cls, v, values):
        assert v >= values['score'] / 200 * 660 * 0.5, \
            f"lifetime should be linear to score"

        assert v >= values['clickRate'] / 3000 * 660 * 0.5, \
            f"lifetime should be linear to clickRate"

        if values['duration'] == 1:
            assert v >= 60 and v % 30 == 0, \
                f"when duration = 1, lifetime >= 60, and lifetime % 30 = 0"
            assert v == 60 + values['batteryTimes'] * 30, \
                f"when duration = 1, lifetime = 60 + batteryTimes * 30"

    @validator('hitRate')
    def validate_hitRate(cls, v, values):
        assert v >= values['score'] / 200 * 1 * 0.5, \
            f"hitRate should be linear to score"

    """
    验证的字段必须出现在需要的字段之后
    """

    @validator('isRealScore')
    def validate_isRealScore(cls, v: FeatIsRealScore, values):
        if values['isUpload'] == 0:
            assert v == FeatIsRealScore.NO_DATA, \
                f"when isUpload = 0, then isRealScore = FeatIsRealScore.NO_DATA, instead of {v}"

    @validator('impulseTimes')
    def validate_impulseTimes(cls, v, values):
        assert v <= (
            values['batteryTimes'] +
            values['filterLenTimes'] +
            values['signalTimes']
        ) >> 1, \
            f"impulseTimes <= 1/2 * (batteryTimes + filterLenTimes + signalTimes)"


if __name__ == '__main__':
    feat = FeatModel(
        storyTime=0.,
        tutorialTime=0.,
        duration=False,
        score=0.,
        difficultyLevel=FeatDifficultyLevel.EASY,
        replayTimes=False,
        hitRate=0.,
        badRate=0.,
        mismatchRate=0.,
        keepaway=0.,
        feedback=0.,
        goodRate=0.,
        moveNum=0.,
        clickRate=0.,
        npcHitRate=0.,
        getbackRate=0.,
        isAcceptGift=False,
        giftType=FeatGiftType.NONE,
        isUpload=False,
        isRealScore=FeatIsRealScore.NO_DATA,
        bugTimes=False,
        batteryTimes=1,
        filterLenTimes=0,
        signalTimes=0,
        impulseTimes=0,
        morePolicy=False,
        lifetime=0,
    )
    logger.info(f'feat: {feat}')
