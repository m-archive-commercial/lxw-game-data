"""
source: own
author: https://github.com/MarkShawn2020
create: Aug 14, 2022, 03:57
"""
import random
from unittest import TestCase

import numpy as np

from ds import FeatRealScore


class TestFeatIsRealScore(TestCase):
    def test_enum(self):

        self.assertEqual([-1, 0, 1], FeatRealScore.values())

        enum_vals = np.random.choice(FeatRealScore.values(), 3)
        print('enum_vals: ', enum_vals)
        self.assertEqual(enum_vals.shape, (3,))
        # iterated unittest, ref: https://stackoverflow.com/a/45736718/9422455
        self.assertTrue(any(v in [0, -1, 1] for v in enum_vals))

        chosen = random.choice(FeatRealScore.values())
        print('chosen: ', chosen)
        self.assertIn(chosen, [-1, 0, 1])
