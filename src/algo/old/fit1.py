"""
source: own
author: https://github.com/MarkShawn2020
create: Aug 14, 2022, 02:03
"""
from typing import List, Union

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


FloatArrayLike = Union[np.array, List[float]]


def func_to_fit(x, a, b, c):
    """
    we can't use polynomial function with levels > 2,
    since it would have a high possibility of getting negative values,
    especially for a large sample on (0, 100, 830, 2000, 3000)
    :param x:
    :param a:
    :param b:
    :param c:
    :return:
    """
    return a + \
           b * x + \
           c * x ** 2  # + \
    # d * x ** 3


def norm_ys(ys: FloatArrayLike) -> np.ndarray:
    ys = np.array(ys)
    return (ys - min(ys)) / (max(ys) - min(ys))


def denorm_ys(y, ys: FloatArrayLike) -> np.ndarray:
    ys = np.array(ys)
    return (y - min(ys)) * (max(ys) - min(ys))


def fit(xs: FloatArrayLike, ys: FloatArrayLike, norm_ys=norm_ys, sigma=None, draw=False):
    xs = np.array(xs)
    ys = norm_ys(np.array(ys))
    p_opt, p_covariance = curve_fit(func_to_fit, xs, ys, sigma=sigma)
    # print({'popt': popt, "covariance": p_covariance})
    if draw:
        xs_plot = np.linspace(0, 1, 100)
        plt.plot(xs_plot, func_to_fit(xs_plot, *p_opt), 'g--',
            label=f'fit: y='
                  f'%5.3f'
                  f' + %5.3fx'
                  f' + %5.3fx^2'
                  # f' + %5.3fx^3'
                  % tuple(p_opt))
        plt.legend()
        plt.show()
    return p_opt


def gen(opts, ys, denorm_ys=denorm_ys, N=500, draw=False) -> np.ndarray:
    print({'ys': ys, 'denorm_ys': denorm_ys, 'opts': opts})
    ys_gen = np.array([denorm_ys(func_to_fit(x, *opts), ys) for x in np.random.random(N)])
    if draw:
        plt.hist(ys_gen, bins=N // 10)
        plt.show()
    return ys_gen


def fit_and_gen(xs, ys, sigma, N) -> np.ndarray:
    return gen(fit(xs, ys, sigma=sigma), ys, N=N)


if __name__ == '__main__':
    xs = (0, 0.25, 0.5, 0.75, 1)
    ys = (0, 5, 10, 30, 100)
    # ys = (0, 100, 830, 2000, 3000)
    # ys = [0, 5, 10, 20, 100]
    opts = fit(xs, ys, draw=True)
    gen(opts, ys, N=500, draw=True)
