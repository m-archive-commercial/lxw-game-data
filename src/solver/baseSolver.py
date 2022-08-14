"""
source: own
author: https://github.com/MarkShawn2020
create: Aug 14, 2022, 23:58
"""
from abc import abstractmethod
from typing import Iterator

import numpy as np

from utils.log import get_logger


logger = get_logger("BaseSolver")


class BaseSolver:

    def __init__(self, xdata: Iterator[float] = None):
        """
        # since we couldn't control the right hand strictly limited to 1,
        # we decreased 1 to be a bit smaller
        :param xdata: 分位数
        """
        self._xdata = xdata or [0, 0.25, 0.5, 0.75, 0.97]
        self._solver = None

    @property
    def xdata(self):
        return self._xdata

    @abstractmethod
    def fit(self, ydata: Iterator[float]):
        raise NotImplementedError('solver not implemented')

    def generate(self, N: int = 1) -> np.ndarray:
        return self._solver(np.random.random(N))
