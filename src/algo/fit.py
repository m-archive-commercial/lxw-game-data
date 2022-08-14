"""
source: own
author: https://github.com/MarkShawn2020
create: Aug 14, 2022, 02:03
"""
import math
from typing import List, Union, Iterator

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

from log import get_logger

logger = get_logger('algo-curve-fit')

FloatArrayLike = Union[np.array, List[float]]


def _to_fit(x, _opts: List[float], _exps: Iterator[int]):
    logger.info({'x': x, "_opts": _opts, "_exps": _exps})
    return sum(opt * x ** exp for (opt, exp) in zip(_opts, _exps))


def get_label(opts):
    return [i.round(3) for i in opts]
    # return 'y = ' + ' + '.join([f'{opt.round(3)}·x^{exp}' for opt, exp in zip(opts, exps + ['log', 'log10'])])


def gen_fitter_eval():
    """
    ref: Python: defining a function with variable number of arguments - Stack Overflow, https://stackoverflow.com/questions/45192234/python-defining-a-function-with-variable-number-of-arguments
    tks: 若哥
    """
    args = ", ".join([f'a{i}' for i in range(len(exps))])
    f = f'lambda x, {args}: _to_fit(x, [{args}], exps)'
    logger.info(f'exec: `{f}`')
    return eval(f)


def norm_ys(ys: FloatArrayLike) -> np.ndarray:
    ys = np.array(ys)
    return (ys - min(ys)) / (max(ys) - min(ys))


def denorm_ys(y, ys: FloatArrayLike) -> np.ndarray:
    ys = np.array(ys)
    return (y - min(ys)) * (max(ys) - min(ys))


def fit(xs: FloatArrayLike, ys: FloatArrayLike, norm_ys=norm_ys,
        sigma=None,
        exps: List[int] = None,
        draw=False
        ):
    xs = np.array(xs)
    ys = norm_ys(np.array(ys))
    try:
        p_opts, p_covariance = curve_fit(to_fit, xs, ys,
            sigma=sigma,
            bounds=(0, np.inf)
        )
        # print({'popt': popt, "covariance": p_covariance})
        if draw:
            xs_plot = np.linspace(0, 1, 100)
            plt.plot(xs_plot, to_fit(xs_plot, *p_opts), 'g--',
                label=get_label(p_opts)
            )
            plt.plot(xs, ys, 'r+')
            plt.suptitle('y to percentiles: ' + ', '.join([str(int(i * 100)) + "%" for i in ys]))
            plt.legend()
            plt.show()
        return p_opts
    except (ValueError, RuntimeError) as e:
        logger.warning(f'ys: {ys}, error: {e}')
        raise e


def gen(opts, ys, denorm_ys=denorm_ys, N=500, draw=False) -> np.ndarray:
    # print({'ys': ys, 'denorm_ys': denorm_ys, 'opts': opts})
    ys_gen = np.array([denorm_ys(to_fit(x, *opts), ys) for x in np.random.random(N)])
    if draw:
        plt.hist(ys_gen, bins=N // 10)
        plt.show()
    return ys_gen


def fit_and_gen(xs, ys, sigma, N) -> np.ndarray:
    return gen(fit(xs, ys, sigma=sigma), ys, N=N)


def gen_sigmoid_any(x1, y1, x2, y2):
    def shadow_inf(x):
        return np.tan((x - (x1 + x2) / 2) / ((x2 - x1) / 2) * np.pi / 2)

    def sigmoid(x):
        return 1 / (1 + np.exp(- shadow_inf(x)))

    return lambda x: y2 * sigmoid(x) + y1 * (1 - sigmoid(x))


def gen_circle_any(x1, y1, x2, y2, x, flip=False):
    u = x - x1
    R = x2 - x1
    v = R - math.sqrt(R ** 2 - u ** 2)
    if flip:
        v = math.sqrt(u * (2 * R - u))
    scale = (y2 - y1) / R
    return y1 + v * scale


def sigmoid_period(xs: List[float], ys: List[float], x: float):
    # ref: https://stackoverflow.com/a/2236935/9422455
    pos = next(xi[0] for xi in enumerate(xs) if xi[1] > x) - 1
    y = gen_circle_any(xs[pos], ys[pos], xs[pos + 1], ys[pos + 1], x, flip=pos % 2 == 1)
    # y = gen_sigmoid_any(xs[pos], ys[pos], xs[pos + 1], ys[pos + 1])(u)
    logger.info({'pos': pos, 'x': x, 'y': y})
    return y


if __name__ == '__main__':
    exps = [1, 3, 7, 15]


    def to_fit(x, a, b, b2, c, d, e, f):
        return \
            + e * np.log(x + 1) / np.log(f + 1) \
            + d / (1 + np.exp(-x * c))
        # + a * x \
        # + b * x ** 2 \
        # + b2 * x ** 3 \
        # + c * x ** 7 \
        # + d * x ** 15


    xs = [0, 0.25, 0.5, 0.75, 0.97]
    sigma = [0.1, 1, 0.1, 1, 0.1]
    # ys = [0, 100, 830, 2000, 3000]
    ys = [0, 5, 10, 20, 100]
    # opts = fit(xs, ys, draw=True, sigma=sigma)
    # gen(opts, ys, N=500, draw=True)

    xs_plot = np.linspace(0, xs[-1], 500, endpoint=False)
    ys_plot = [sigmoid_period(xs, ys, x) for x in xs_plot]
    # logger.info({'xs_plot': xs_plot, 'ys_plot': ys_plot})
    plt.plot(xs_plot, ys_plot, 'g-')
    plt.plot(xs, ys, 'r+')
    plt.show()


# [0.    0.025 0.2   0.5   1.   ] -- 1 2 4
# [0.         0.03333333 0.27666667 0.66666667 1.        ] -- 1 3 9
