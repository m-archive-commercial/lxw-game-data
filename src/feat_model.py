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

        fScore --> pctHitRate
        fScore, intClickFreq, isDuration, intBatteryTimes --> intLifetime
        intBatteryTimes, intFilterLenTimes, intSignalTimes --> intImpulseTimes
        isUpload --> enumRealScore

    todo:
        1. add help/description on each field
        2. add stat constraint
    """

    fScore: strict_float(le=FEAT_SCORE_MAX)  # (5, 40, 100)

    pctHitRate: strict_percent()

    intClickFreq: strict_int(le=FEAT_CLICKRATE_MAX)  # (100, 830, 2000)
    isDuration: int  # bool # 0. 中途退出，1. 坚持最后
    intBatteryTimes: strict_int(le=FEAT_BATTERYTIME_MAX)  # (0, 2, 5)

    intLifetime: strict_int(le=FEAT_LIFETIME_MAX)  # max: 660

    intFilterLenTimes: strict_int(le=FEAT_FILTERLENTIMES)  # (0,2,5)
    intSignalTimes: strict_int(le=FEAT_SIGNALTIMES_MAX)  # (0,2,5)
    intImpulseTimes: strict_int(le=FEAT_IMPULSETIMES_MAX)  # (0, 2,5)

    isUpload: int  # bool
    enumRealScore: FeatRealScore

    fStoryTime: strict_float(le=FEAT_STORYTIME_MAX)  # (5, 10, 30)
    fTutorialTime: strict_float(le=FEAT_TUTORIALTIME_MAX)  # (5, 18, 40)
    enumDifficultyLevel: FeatDifficultyLevel
    isReplayed: int  # bool # 0. 不重玩 1. 重玩
    pctBadRate: strict_percent()
    pctMismatchRate: strict_percent()
    fKeepaway: strict_float(le=FEAT_KEEPAWAY_MAX)  # (5, 60, 100)
    pctFeedback: strict_percent()
    pctGoodRate: strict_percent()
    fMoveNum: strict_float(le=FEAT_MOVENUM_MAX)  # (5, 40, 100)
    pctNpcHitRate: strict_percent()
    pctGetbackRate: strict_percent()
    isAcceptGift: int  # bool
    enumGiftType: FeatGiftType
    isBug: int  # bool
    isMorePolicy: int  # bool

    @validator('pctHitRate')
    def validate_hitRate(cls, v, values):
        validateHitRate(v, values)
        return v

    @validator('enumRealScore')
    def validate_realScore(cls, v, values):
        validateRealScore(v, values)
        return v

    @validator('intImpulseTimes')
    def validate_impulseTimes(cls, v, values):
        validateImpulseTimes(v, values)
        return v

    @validator('intLifetime')
    def validate_lifetime(cls, v, values):
        validateLifetime(v, values)
        return v


if __name__ == '__main__':
    feat = FeatModel(
        isDuration=False,
        isReplayed=False,
        isAcceptGift=False,
        isUpload=False,
        isBug=False,
        isMorePolicy=False,

        enumDifficultyLevel=FeatDifficultyLevel.EASY,
        enumGiftType=FeatGiftType.NONE,
        enumRealScore=FeatRealScore.NO_DATA,

        intBatteryTimes=1,
        intFilterLenTimes=0,
        intSignalTimes=0,
        intImpulseTimes=0,
        intLifetime=0,
        intClickFreq=0,

        fStoryTime=0.,
        fTutorialTime=0.,
        fScore=0.,
        fKeepaway=0.,
        fMoveNum=0.,

        pctHitRate=0.,
        pctBadRate=0.,
        pctMismatchRate=0.,
        pctFeedback=0.,
        pctGoodRate=0.,
        pctNpcHitRate=0.,
        pctGetbackRate=0.,
    )
    logger.info(f'feat: {feat}')
