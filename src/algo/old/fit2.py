"""
source: own
author: https://github.com/MarkShawn2020
create: Aug 14, 2022, 02:03
"""
from typing import List, Union

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

from log import get_logger

logger = get_logger('algo-curve-fit')

FloatArrayLike = Union[np.array, List[float]]

exps = [1, 2, 3, 4]


class FitSolver:

    def __init__(self, xs, ys, N=500, sigma=None, bounds=None):
        self._xs = np.array(xs or (0, 0.25, 0.5, 0.75, 0.97))
        self._ys = np.array(ys)
        self._ysn = (self._ys - min(self._ys)) / (max(self._ys) - min(self._ys))
        self._N = N
        self._sigma = sigma or (0.1, 1, 0.1, 1, 0.1)
        self._bounds = bounds or (0, np.inf)

        self._fitter_exp = self._ys[-1] // self._ys[-2]
        self._fitter_exps = [(self._fitter_exp + 1) ** i for i in range(3)]
        self._fitter_func = lambda x, *args: sum(abs(arg * x ** exp) for arg, exp in zip(args, exps))

        self._opts = None

    def denorm_ys(self, y) -> np.ndarray:
        return (y - min(self._ys)) * (max(self._ys) - min(self._ys))

    def fit(self, draw=False):
        try:
            p_opt, p_covariance = curve_fit(
                self._fitter_func,
                self._xs,
                self._ys,
                sigma=self._sigma,
                bounds=self._bounds
            )
            if draw:
                xs_plot = np.linspace(0, 1, 100)
                plt.plot(xs_plot, self._fitter_func(xs_plot, *p_opt), 'g--',
                    label='y = ' + ' + '.join([f"|{i.round(3)}x^{exps[_]}|" for _, i in enumerate(p_opt)]))
                plt.plot(xs, ys, 'r+')
                plt.suptitle('y to percentiles: ' + ', '.join([str(int(i * 100)) + "%" for i in ys]))
                plt.legend()
                plt.show()
            self._opts = p_opt
            return p_opt
        except (ValueError, RuntimeError) as e:
            logger.warning(f'ys: {ys}, error: {e}')
            raise e


    def gen(self, draw=False) -> np.ndarray:
        # print({'ys': ys, 'denorm_ys': denorm_ys, 'opts': opts})
        ys_gen = np.array([self.denorm_ys(self._fitter_func(x, *self._opts)) for x in np.random.random(self._N)])
        if draw:
            plt.hist(ys_gen, bins=self._N // 10)
            plt.show()
        return ys_gen


    def fit_and_gen(self) -> np.ndarray:
        return self.gen(self.fit())


if __name__ == '__main__':
    xs = (0, 0.25, 0.5, 0.75, 0.97)
    sigma = (0.1, 1, 0.1, 1, 0.1)
    ys = (0, 100, 830, 2000, 3000)
    # ys = [0, 5, 10, 20, 100]
    solver = FitSolver(xs, ys, sigma=sigma)
    solver.fit(draw=True)
    # gen(opts, ys, N=500, draw=True)


# [0.    0.025 0.2   0.5   1.   ] -- 1 2 4
# [0.         0.03333333 0.27666667 0.66666667 1.        ] -- 1 3 9
