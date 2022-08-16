"""
source: own
author: https://github.com/MarkShawn2020
create: Aug 14, 2022, 23:58
"""
import matplotlib.pyplot as plt
import numpy as np

from config.model import DEFAULT_XDATA
from utils.algo import peak
from utils.log import get_logger


logger = get_logger("BaseSolver")


class BaseSolver:

    def __init__(
        self,
    ):
        self._xdata = DEFAULT_XDATA
        self._ydata = None
        self._peakRatio = 0

        self._x2y = None

    @property
    def xdata(self):
        return self._xdata

    @property
    def _yMin(self):
        return self._ydata[0]

    @property
    def _yMax(self):
        return self._ydata[-1]

    @property
    def _yMean(self):
        """
        todo: median --> mean
        :return:
        """
        return self._ydata[len(self._ydata) >> 1]

    @property
    def _xMin(self):
        return self._xdata[0]

    @property
    def _xMax(self):
        return self._xdata[-1]

    def setMainSpace(self, v):
        """
        设置核心区域对定义域的占比
        :param v: [0, 1], default: 0.5
        :return:
        """
        assert 0 < v < 1, f'should 0 < v < 1, otherwise fitted result is possible unexpected'
        self._xdata = [0, .5 - v / 2, .5, .5 + v / 2, 1]
        logger.debug(f'xdata: {self._xdata}')
        return self

    def setPeakRatio(self, v):
        self._peakRatio = v
        return self

    def setXdata(self, v):
        self._xdata = v
        return self

    def setYdata(self, v):
        self._ydata = v
        return self

    def setPCF(self, pcf):
        def pcf2xy(x):
            ratioFromLeft = pcf(peak(x, self._peakRatio))
            return self._yMin * (1 - ratioFromLeft) + ratioFromLeft * self._yMax

        self._x2y = pcf2xy
        return self

    def fit(self):
        raise NotImplementedError

    def generate(self, N: int) -> np.ndarray:
        """

        :param N:
        :param toPeak: [0, 1], default: 0.5
        :return:
        """
        # ref: https://stackoverflow.com/questions/35215161/most-efficient-way-to-map-function-over-numpy-array
        return self._x2y(np.random.random(N))

    def plotBoth(self, nFit=100, nGen=1000, bins=100, toPeak=None):
        fig, axes = plt.subplots(2, 1)
        # for pcf, domain is (0, 1)
        xdata = np.linspace(0, 1, nFit, endpoint=False)
        ydata = self._x2y(xdata)
        axes[0].plot(xdata, ydata, 'g-')
        axes[0].plot(self._xdata, self._ydata, 'r+')

        ydata = self.generate(nGen)
        axes[1].hist(ydata, bins)

        plt.suptitle(f'xdata: {self._xdata}, ydata: {self._ydata}')
        plt.show()

    def plotSolver(self, N=100):
        xdata = np.linspace(0, 1, N, endpoint=False)
        ydata = self._x2y(xdata)
        plt.plot(xdata, ydata, 'g-')
        plt.plot(self._xdata, self._ydata, 'r+')
        plt.show()
        return self

    def plotSample(self, N=500, bins=50):
        ydata = self.generate(N)
        plt.hist(ydata, bins=bins)
        plt.show()
        return self


"""
do not directly test on BaseSolver

since the `solver` should be extended to be implemented
"""
