"""
source: own
author: https://github.com/MarkShawn2020
create: Aug 14, 2022, 06:34
"""
from unittest import TestCase

import numpy as np

from feat_generator import FeatGenerator


class TestFeatGenerator(TestCase):
    def test__gen_floats(self):
        feat_generator = FeatGenerator()
        v = feat_generator._gen_floats((0, 100, 830, 2000, 3000))
        print(v)
        self.assertEqual(len(v[v > 0]), 500)

