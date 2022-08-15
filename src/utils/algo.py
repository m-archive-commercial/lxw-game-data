"""
source: own
author: https://github.com/MarkShawn2020
create: Aug 16, 2022, 07:15
"""
import matplotlib.pyplot as plt
import numpy as np
from numpy import exp


def peak(x, ratio, scale=3, flip=False):
    """
    @:param ratio
    todo: inverse function
    """
    if flip:
        raise NotImplementedError
    assert 0 <= ratio <= 1

    # convert to (-1, 1)
    x = x * 2 - 1

    ratio = exp(ratio * scale) - 1 + .1
    # 双曲余弦函数
    v = x * (exp(ratio * x) + exp(-ratio * x)) / (exp(ratio) + exp(-ratio))
    v = (v + 1) / 2
    return v


if __name__ == '__main__':
    xs = np.linspace(0, 1, 100)
    for i in np.linspace(0, 1, 10):
        ys = peak(xs, i)
        plt.plot(xs, ys, color=(i, 0, 0))
    plt.show()
