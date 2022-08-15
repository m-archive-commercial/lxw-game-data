"""
source: own
author: https://github.com/MarkShawn2020
create: Aug 16, 2022, 04:31
"""
import matplotlib.pyplot as plt
import numpy as np
from numpy import exp


def bend(x, k, scale=3, flip=False):
    """
    todo: inverse function
    """
    print(k, end='\t-->\t')
    if flip:
        raise NotImplementedError
    k = exp(k * scale) - 1 + .1
    print(k)
    # ratio = np.log(ratio*scale+1)
    # 双曲余弦函数
    # ratio = np.log(ratio * 10000 + 1) / np.log(100)
    v = (exp(k * x) + exp(-k * x)) / (exp(k) + exp(-k))
    return x * v


xs = np.linspace(-1, 1, 100)
ys = xs
N = 30
for i in np.linspace(0, 1, N, endpoint=False):
    plt.plot(xs, bend(ys, i), color=(1, i, i))
plt.plot(xs, bend(ys, .99), 'b')
plt.plot(xs, ys, 'm-')
plt.show()
