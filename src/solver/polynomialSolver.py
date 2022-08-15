"""
source: own
author: https://github.com/MarkShawn2020
create: Aug 15, 2022, 00:01
"""
from typing import Iterator, Callable, Any

import numpy as np
from scipy.optimize import curve_fit

from solver.baseSolver import BaseSolver
from utils.log import get_logger

logger = get_logger('PolynomialSolver')


class PolynomialSolver(BaseSolver):

    def fit(
        self,
        func: Callable = None,
        sigma: Iterator[float] = None,
        bounds: Any = None,
    ):
        if not func:
            func = lambda x, a1, a2, a3: a1 * x + a2 * x ** 3 + a3 ** 7
        if not bounds:
            bounds = [0, np.inf]  # positive
        opts, covariance = curve_fit(func, xdata=self._xdata, ydata=self._ydata, sigma=sigma, bounds=bounds)
        logger.debug(f'opts: {opts}')
        self._x2y = lambda x: func(x, *opts)
        return self


if __name__ == '__main__':
    gSolver = PolynomialSolver()
    gSolver \
        .setMainSpace(0.5) \
        .setYdata([0, 1, 2, 5, 100]) \
        .fit() \
        .plotBoth(nFit=500, nGen=500, toPeak=.9)
