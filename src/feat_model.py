"""
source: own
author: https://github.com/MarkShawn2020
create: Aug 13, 2022, 22:31
"""

from pydantic import BaseModel, validator

from config.feats import FEAT_TUTORIALTIME_MAX, FEAT_STORYTIME_MAX, FEAT_MOVENUM_MAX, FEAT_KEEPAWAY_MAX, \
    FEAT_SCORE_MAX, FEAT_CLICKRATE_MAX, FEAT_IMPULSETIMES_MAX, FEAT_SIGNALTIMES_MAX, FEAT_FILTERLENTIMES, \
    FEAT_BATTERYTIME_MAX, FEAT_LIFETIME_MAX
from ds import FeatDifficultyLevel, FeatGiftType, FeatRealScore
from utils.log import get_logger
from utils.strict_feilds import strict_int, strict_float, strict_percent
from utils.validator_feats import validateLifetime, validateHitRate, validateRealScore, validateImpulseTimes

logger = get_logger("FeatModel")


class FeatModel(BaseModel):
    """
    验证的字段必须出现在需要的字段之后

        score --> hitRate
        score, clickRate, duration, batteryTimes --> lifetime
        batteryTimes, filterLenTimes, signalTimes --> impulseTimes
        isUpload --> realScore

    todo:
        1. add help/description on each field
        2. add stat constraint
    """

    score: strict_float(le=FEAT_SCORE_MAX)  # (5, 40, 100)

    hitRate: strict_percent()

    clickRate: strict_int(le=FEAT_CLICKRATE_MAX)  # (100, 830, 2000)
    duration: bool  # 0. 中途退出，1. 坚持最后
    batteryTimes: strict_int(le=FEAT_BATTERYTIME_MAX)  # (0, 2, 5)

    lifetime: strict_int(le=FEAT_LIFETIME_MAX)  # max: 660

    filterLenTimes: strict_int(le=FEAT_FILTERLENTIMES)  # (0,2,5)
    signalTimes: strict_int(le=FEAT_SIGNALTIMES_MAX)  # (0,2,5)
    impulseTimes: strict_int(le=FEAT_IMPULSETIMES_MAX)  # (0, 2,5)

    isUpload: bool
    realScore: FeatRealScore

    storyTime: strict_float(le=FEAT_STORYTIME_MAX)  # (5, 10, 30)
    tutorialTime: strict_float(le=FEAT_TUTORIALTIME_MAX)  # (5, 18, 40)
    difficultyLevel: FeatDifficultyLevel
    replayTimes: bool  # 0. 不重玩 1. 重玩
    badRate: strict_percent()
    mismatchRate: strict_percent()
    keepaway: strict_float(le=FEAT_KEEPAWAY_MAX)  # (5, 60, 100)
    feedback: strict_percent()
    goodRate: strict_percent()
    moveNum: strict_float(le=FEAT_MOVENUM_MAX)  # (5, 40, 100)
    npcHitRate: strict_percent()
    getbackRate: strict_percent()
    isAcceptGift: bool
    giftType: FeatGiftType
    bugTimes: bool
    morePolicy: bool

    @validator('hitRate')
    def validate_hitRate(cls, v, values):
        validateHitRate(v, values)
        return v

    @validator('realScore')
    def validate_realScore(cls, v, values):
        validateRealScore(v, values)
        return v

    @validator('impulseTimes')
    def validate_impulseTimes(cls, v, values):
        validateImpulseTimes(v, values)
        return v

    @validator('lifetime')
    def validate_lifetime(cls, v, values):
        validateLifetime(v, values)
        return v


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
        realScore=FeatRealScore.NO_DATA,
        bugTimes=False,
        batteryTimes=1,
        filterLenTimes=0,
        signalTimes=0,
        impulseTimes=0,
        morePolicy=False,
        lifetime=0,
    )
    logger.info(f'feat: {feat}')
