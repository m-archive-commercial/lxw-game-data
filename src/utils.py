"""
source: own
author: https://github.com/MarkShawn2020
create: Aug 14, 2022, 04:41
"""
import random

import numpy as np

from feat_model import FeatIsRealScore


def battery2LifeTime(batteryTime: np.ndarray) -> np.ndarray:
    """
    np.where, ref: https://numpy.org/doc/stable/reference/generated/numpy.where.html
    :param batteryTime:
    :return:
    """
    return np.where(
        batteryTime > 0,
        60 + 30 * batteryTime,
        int(random.random() * 60)
    )


def upload2score(isUpload: np.ndarray) -> np.ndarray:
    return np.where(
        isUpload == 0,
        FeatIsRealScore.NO_DATA,
        random.choice(FeatIsRealScore.values())
    )
