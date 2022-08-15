"""
source: own
author: https://github.com/MarkShawn2020
create: Aug 15, 2022, 16:09
"""
import argparse

from config.model import DEFAULT_NUM_MODELS_TO_GEN
from feat_generator import FeatGenerator
from solver.baseSolver import BaseSolver
from solver.polynomialSolver import PolynomialSolver

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-n', '--nModelsToGen', default=DEFAULT_NUM_MODELS_TO_GEN, type=int,
        help='number of target models to be generated, e.g. 500'
    )
    parser.add_argument(
        '--nMaxGenRetries', default=10,
        help='number of retrying to generate models in each epoch, recommending 5-10'
    )
    parser.add_argument(
        '-d', '--dump', action='store_true',
        help='dump the feature models to file'
    )
    args = parser.parse_args()

    gSolver: BaseSolver = PolynomialSolver()
    gFeatGenerator = FeatGenerator(
        gSolver,
        nModelsToGen=args.nModelsToGen,
        nMaxGenRetries=args.nMaxGenRetries
    ).genFeatModels()
    if args.dump:
        gFeatGenerator.dump()
