"""
source: own
author: https://github.com/MarkShawn2020
create: Aug 14, 2022, 04:41
"""
from unittest import TestCase

import numpy as np

from src.utils import battery2LifeTime


class Test(TestCase):
    def test_battery2life_time(self):
        lifetime = battery2LifeTime(np.array([0, 0, 1, 20]))
        self.assertEqual(lifetime[2], 90)
        self.assertEqual(lifetime[3], 660)
        self.assertLessEqual(lifetime[0], 60)
        self.assertLessEqual(lifetime[1], 60)
