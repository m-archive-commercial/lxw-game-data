"""
source: own
author: https://github.com/MarkShawn2020
create: Aug 16, 2022, 01:13
"""
import numpy as np

from solver.baseSolver import BaseSolver
from utils.log import get_logger


logger = get_logger('LinearSmoothSolver')


class LinearSmoothSolver(BaseSolver):

    def fit(self):
        def PCF(x_in):
            def getY(x_in_single):
                # p: right index of located period
                p = next(i for i, x in enumerate(self._xdata) if x >= x_in_single)
                ratioFromLeft = (x_in_single - self._xdata[p - 1]) / (self._xdata[p] - self._xdata[p - 1])
                y = (1 - ratioFromLeft) * self._ydata[p - 1] + ratioFromLeft * self._ydata[p]
                return y

            return (np.vectorize(getY)(x_in) - self._yMin) / (self._yMax - self._yMin)

        self.setPCF(PCF)
        return self


if __name__ == '__main__':
    gSolver = LinearSmoothSolver()
    gSolver \
        .setMainSpace(.5) \
        .setPeakRatio(.1) \
        .setYdata([0, 1, 2, 5, 100]) \
        .fit() \
        .plotBoth(nFit=500, nGen=1000, bins=100)
