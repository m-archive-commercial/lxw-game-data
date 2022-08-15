"""
source: own
author: https://github.com/MarkShawn2020
create: Aug 14, 2022, 23:58
"""
from abc import abstractmethod

import matplotlib.pyplot as plt
import numpy as np

from config.model import DEFAULT_XDATA
from utils.log import get_logger


logger = get_logger("BaseSolver")


class BaseSolver:

    def __init__(
        self,
    ):
        """
        # since we couldn't control the right hand strictly limited to 1,
        # we decreased 1 to be a bit smaller
        :param xdata: 分位数
        """
        self._solver = None
        self._xdata = None
        self._ydata = None

        self.initX()

    def initX(self, xdata=None):
        self._xdata = xdata or DEFAULT_XDATA
        return self

    def initY(self, ydata):
        self._ydata = ydata
        return self

    @property
    def xdata(self):
        return self._xdata

    @abstractmethod
    def fit(self):
        raise NotImplementedError('solver not implemented')

    def generate(self, N: int = 1) -> np.ndarray:
        return self._solver(np.random.random(N))

    def plotSolver(self, N=100):
        xdata = np.linspace(0, self.xdata[-1], N, endpoint=False)
        ydata = self._solver(xdata)
        plt.plot(xdata, ydata, 'g-')
        plt.plot(self.xdata, self._ydata, 'r+')
        plt.show()

    def plotSample(self, N=500, bins=50):
        ydata = self.generate(N)
        plt.hist(ydata, bins=50)
        plt.show()
