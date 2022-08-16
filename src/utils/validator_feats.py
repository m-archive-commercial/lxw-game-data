"""
source: own
author: https://github.com/MarkShawn2020
create: Aug 15, 2022, 00:46
"""
from config.feats import FEAT_HITRATE_MAX
from ds import FeatRealScore


def validateHitRate(v, values):
    pass
    # assert v >= values['fScore'] / 200 * FEAT_HITRATE_MAX * 0.5, \
    #     f"hitRate should be linear to fScore"


def validateRealScore(v, values):
    if not values['isUpload']:
        assert v == FeatRealScore.NO_DATA, \
            f"when isUpload = 0, should realScore({v}) = FeatIsRealScore.NO_DATA"


def validateImpulseTimes(v, values):
    pass
    # assert v <= (values['intBatteryTimes'] + values['intFilterLenTimes'] + values['intSignalTimes']) >> 1, \
    #     f"impulseTimes({v}) <= 1/2 * (" \
    #     f"intBatteryTimes({values['intBatteryTimes']}) " \
    #     f"+ intFilterLenTimes({values['intFilterLenTimes']}) " \
    #     f"+ intSignalTimes({values['intSignalTimes']})" \
    #     f")"


def validateLifetime(v, values, linear_ratio=0.3):
    # assert v >= values['fScore'] / 200 * 660 * linear_ratio, \
    #     f"lifetime({v}) should be linear to fScore({values['fScore']})"

    # assert v >= values['intClickFreq'] / 3000 * 660 * linear_ratio, \
    #     f"lifetime({v}) should be linear to intClickFreq({values['intClickFreq']})"

    if values['isDuration'] == 1:
        assert v >= 60 and v % 30 == 0, \
            f"when isDuration = 1, should lifetime({v}) >= 60, and lifetime({v}) % 30 = 0"
        assert v == 60 + values['intBatteryTimes'] * 30, \
            f"when isDuration = 1, should lifetime({v}) = 60 + intBatteryTimes({values['intBatteryTimes']}) * 30"
