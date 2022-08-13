"""
source: own
author: https://github.com/MarkShawn2020
create: Aug 13, 2022, 22:31
"""
from enum import Enum

from pydantic import BaseModel, confloat, conint


class FeatDifficultyLevel(int, Enum):
    EAST = 0
    MID = 1
    HARD = 2


class FeatGiftType(int, Enum):
    GOOD = 0
    BAD = 1
    NONE = 2


class FeatIsRealScore(int, Enum):
    NO_DATA = -1
    DATA_SAME = 0
    DATA_DIFF = 1


def conpercent():
    return confloat(strict=True, ge=0, le=1)


class FeatureModel(BaseModel):
    """
    todo:
        1. add help/description on each field
        2. add stat constraint
    """

    storyTime: confloat(strict=True, ge=0, le=100)  # 平均10，通常5-30
    tutorialTime: confloat(strict=True, ge=0, le=100)  # 平均18，通常5-40
    duration: bool  # 0. 中途退出，1. 坚持最后
    score: confloat(strict=True, ge=0, le=200)  # 平均40，通常5-100
    difficultyLevel: FeatDifficultyLevel
    replayTimes: bool  # 0. 不重玩 1. 重玩
    hitRate: conpercent()
    badRate: conpercent()
    mismatchRate: conpercent()
    keepaway: confloat(ge=0, le=200)
    feedback: conpercent()
    goodRate: conpercent()
    moveNum: confloat(ge=0, le=200)
    clickRate: confloat(ge=0, le=3000)
    npcHitRate: conpercent()
    getbackRate: conpercent()
    isAcceptGift: bool
    giftType: FeatGiftType
    isUpload: bool
    isRealScore: FeatIsRealScore
    bugTimes: bool
    batteryTimes: conint(ge=0, le=20)
    filterLenTimes: conint(ge=0, le=20)
    signalTimes: conint(ge=0, le=20)
    impulseTimes: conint(ge=0, le=20)
    morePolicy: bool
    lifetime: conint(ge=0, le=5 * 60)  # max: 5 min


if __name__ == '__main__':
    feat = FeatureModel(
        storyTime=0.,
        tutorialTime=0.,
        duration=0,
        score=0.,
        difficultyLevel=0,
        replayTimes=0,
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
        isAcceptGift=0,
        giftType=0,
        isUpload=0,
        isRealScore=0,
        bugTimes=0,
        batteryTimes=0,
        filterLenTimes=0,
        signalTimes=0,
        impulseTimes=0,
        morePolicy=0,
        lifetime=0,
    )
    print('feat', feat)
