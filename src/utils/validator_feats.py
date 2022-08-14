"""
source: own
author: https://github.com/MarkShawn2020
create: Aug 15, 2022, 00:46
"""
from .ds import FeatRealScore


def validateHitRate(v, values):
    assert v >= values['score'] / 200 * 1 * 0.5, \
        f"hitRate should be linear to score"


def validateRealScore(v: FeatRealScore, values):
    if values['isUpload'] == 0:
        assert v == FeatRealScore.NO_DATA, \
            f"when isUpload = 0, should isRealScore({v}) = FeatIsRealScore.NO_DATA"


def validateImpulseTimes(v, values):
    assert v <= (
        values['batteryTimes'] +
        values['filterLenTimes'] +
        values['signalTimes']
    ) >> 1, \
        f"impulseTimes({v}) <= 1/2 * (" \
        f"batteryTimes({values['batteryTimes']}) " \
        f"+ filterLenTimes({values['filterLenTimes']}) " \
        f"+ signalTimes({values['signalTimes']})" \
        f")"


def validateLifetime(v, values, linear_ratio=0.3):
    assert v >= values['score'] / 200 * 660 * linear_ratio, \
        f"lifetime({v}) should be linear to score({values['score']})"

    assert v >= values['clickRate'] / 3000 * 660 * linear_ratio, \
        f"lifetime({v}) should be linear to clickRate({values['clickRate']})"

    if values['duration'] == 1:
        assert v >= 60 and v % 30 == 0, \
            f"when duration = 1, should lifetime({v}) >= 60, and lifetime({v}) % 30 = 0"
        assert v == 60 + values['batteryTimes'] * 30, \
            f"when duration = 1, should lifetime({v}) = 60 + batteryTimes({values['batteryTimes']}) * 30"
