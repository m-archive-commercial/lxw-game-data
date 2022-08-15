"""
source: own
author: https://github.com/MarkShawn2020
create: Aug 16, 2022, 01:13
"""
import numpy as np
from scipy.optimize import curve_fit

from solver.baseSolver import BaseSolver


class UltimateSmoothSolver(BaseSolver):

    def __init__(self):
        super().__init__()

    def fit(self):
        p_opts, p_covariance = curve_fit(
            self._to_fit,
            self._xdata,
            self._ydata,
            bounds=(0, np.inf)
        )
        self._x2y = lambda x: self._to_fit(x, *p_opts)
        return self

    def _to_fit(self, x, a1, a2, a3, a4, a5):
        """
        tks: 旭神
        """

        def S(x, k=30):
            return 1 / (1 + np.exp(-x * k))

        return a1 * S((x - self._xdata[0])) + \
               a2 * S((x - self._xdata[1])) + \
               a3 * S((x - self._xdata[2])) + \
               a4 * S((x - self._xdata[3])) + \
               a5 * S((x - self._xdata[4]))


if __name__ == '__main__':
    gSolver = UltimateSmoothSolver()
    gSolver \
        .setMainSpace(.1) \
        .setYdata([0, 1, 2, 5, 10]) \
        .fit() \
        .plotBoth(nFit=500, nGen=1000, bins=100)
