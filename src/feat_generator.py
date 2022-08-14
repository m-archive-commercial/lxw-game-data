"""
source: own
author: https://github.com/MarkShawn2020
create: Aug 14, 2022, 00:36
"""
from __future__ import annotations

import argparse
from typing import List, Type

import numpy as np
import pandas as pd
import tqdm

from config.model import DEFAULT_XDATA
from ds import ExtendedEnum, FeatDifficultyLevel, FeatGiftType, FeatRealScore
from feat_model import FeatModel
from solver.baseSolver import BaseSolver
from solver.polynomialSolver import PolynomialSolver
from utils.config_path import OUTPUT_DIR
from utils.log import get_logger
from utils.regenerate_field import regenerate
from utils.validator_feats import validateHitRate, validateImpulseTimes, validateLifetime

logger = get_logger('FeatGenerator')


class FeatGenerator:

    def __init__(
        self,
        solver: BaseSolver,
        nTargetModelsValid=500,
        nTargetModelsEpoch=1,
        nMaxGenerateRetries=10
    ):
        """

        :param solver:
        :param nTargetModelsEpoch:
        :param nMaxGenerateRetries: tested: when 5, then failed [88/500]
        """
        self._solver = solver
        self.nTargetModelsValid = nTargetModelsValid
        self.nTargetModelsEpoch = nTargetModelsEpoch
        self.nMaxGenerateRetries = nMaxGenerateRetries

        self._feat_models: List[FeatModel] = []

        logger.debug(f'solver: {self._solver}, target_models_cnt: {self.nTargetModelsEpoch}')

    def _gen_floats(self, ys):
        return self._solver.fit(ys).generate(self.nTargetModelsEpoch)

    def _gen_ints(self, ys):
        """
        tip: here we can use .astype(int) since we didn't use the `StrictInt`
        :param ys:
        :return:
        """
        return self._gen_floats(ys).astype(int)

    def _gen_percents(self):
        """
        percent can be generated linearly, which is the same args like `xdata`
        :return:
        """
        return self._gen_floats(self._solver.xdata)

    def _gen_bools(self):
        return np.random.random(self.nTargetModelsEpoch) > 0.5

    def _gen_choices(self, choices: Type[ExtendedEnum]):
        """
        :param choices: Type[Enum] need
        :return:
        """
        return np.random.choice(choices, self.nTargetModelsEpoch)

    def _genFeatOfLifetime(self, batteryTimes):
        """
        need to be manually aligned
        :param v:
        :return:
        """
        if batteryTimes > 0:
            return 60 + batteryTimes * 30
        return regenerate(
            lambda: self._gen_ints(60),
            lambda v: True
        )

    def _genFeatOfRealScore(self, isUpload):
        if isUpload == 0:
            return FeatRealScore.NO_DATA
        return self._gen_choices(FeatRealScore)[0]

    def preGenFeatModel(self, have_tried=0):
        """
        score --> hitRate
        score, clickRate, duration, batteryTimes --> lifetime
        batteryTimes, filterLenTimes, signalTimes --> impulseTimes
        """
        assert have_tried < self.nMaxGenerateRetries, f"gen featModel failed for {self.nMaxGenerateRetries} tries"

        score = self._gen_floats((0, 5, 40, 100, 200))[0]
        hitRate = self._gen_percents()[0]

        batteryTimes = self._gen_ints((0, 0, 2, 5, 20))[0]
        filterLenTimes = self._gen_ints((0, 1, 2, 5, 20))[0]
        signalTimes = self._gen_ints((0, 1, 2, 5, 20))[0]
        impulseTimes = self._gen_ints((0, 1, 2, 5, 20))[0]

        clickRate = self._gen_floats((0, 100, 830, 2000, 3000))[0]
        duration = self._gen_bools()[0]
        lifetime = self._genFeatOfLifetime(batteryTimes)

        isUpload = self._gen_bools()[0]
        realScore = self._genFeatOfRealScore(isUpload)

        try:
            validateHitRate(hitRate, {'score': score})
            validateImpulseTimes(impulseTimes, {
                "batteryTimes"  : batteryTimes,
                "filterLenTimes": filterLenTimes,
                "signalTimes"   : signalTimes
            })
            validateLifetime(lifetime, {
                "score"       : score,
                "clickRate"   : clickRate,
                "duration"    : duration,
                "batteryTimes": batteryTimes
            })
        except Exception as e:
            return self.preGenFeatModel(have_tried + 1)
        else:
            return {
                "score"         : score,
                "hitRate"       : hitRate,
                "batteryTimes"  : batteryTimes,
                "filterLenTimes": filterLenTimes,
                "signalTimes"   : signalTimes,
                "impulseTimes"  : impulseTimes,
                "clickRate"     : clickRate,
                "duration"      : duration,
                "lifetime"      : lifetime,
                "isUpload"      : isUpload,
                "realScore"     : realScore,
            }

    def genFeatModel(self) -> FeatModel:

        predata = self.preGenFeatModel()

        data = dict(
            **predata,
            storyTime=self._gen_floats((0, 5, 10, 30, 100))[0],
            tutorialTime=self._gen_floats((0, 5, 18, 40, 100))[0],
            difficultyLevel=self._gen_choices(FeatDifficultyLevel)[0],
            replayTimes=self._gen_bools()[0],
            badRate=self._gen_percents()[0],
            mismatchRate=self._gen_percents()[0],
            keepaway=self._gen_floats((0, 5, 60, 100, 200))[0],
            feedback=self._gen_percents()[0],
            goodRate=self._gen_percents()[0],
            moveNum=self._gen_floats((0, 5, 40, 100, 200))[0],
            npcHitRate=self._gen_percents()[0],
            getbackRate=self._gen_percents()[0],
            isAcceptGift=self._gen_bools()[0],
            giftType=self._gen_choices(FeatGiftType)[0],
            bugTimes=self._gen_bools()[0],
            morePolicy=self._gen_bools()[0],
        )
        feat_model = FeatModel(**data)
        self._feat_models.append(feat_model)
        logger.debug(f'generated feat model: {feat_model}')
        return feat_model

    def genFeatModels(self) -> FeatGenerator:
        total_tries = 0
        failed_tries = 0
        for _ in tqdm.tqdm(range(self.nTargetModelsValid)):
            while True:
                try:
                    total_tries += 1
                    self.genFeatModel()
                except:
                    failed_tries += 1
                else:
                    break
        logger.info({
            "config": {
                "target models": self.nTargetModelsValid,
                "max retries"  : self.nMaxGenerateRetries,
            },
            "tries" : {
                "failed": failed_tries,
                "total" : total_tries
            }
        })
        return self

    def dump(self):
        df = pd.DataFrame([dict(i) for i in self._feat_models])
        fp = OUTPUT_DIR / 'feat_models.csv'
        df.to_csv(fp.__str__(), encoding='utf_8', )
        logger.info(f'dumped to file://{fp}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-n', '--nTargetModelsValid', default=10, type=int,
        help='number of target models to be generated, e.g. 500'
    )
    parser.add_argument(
        '-d', '--dump', action='store_true',
        help='dump the feature models to file'
    )
    parser.add_argument(
        '--nMaxGenerateRetries', default=10,
        help='number of retrying to generate models in each epoch, recommending 5-10'
    )
    args = parser.parse_args()

    gSolver: BaseSolver = PolynomialSolver(xdata=DEFAULT_XDATA)
    gFeatGenerator = FeatGenerator(
        gSolver,
        nTargetModelsValid=args.nTargetModelsValid,
        nMaxGenerateRetries=args.nMaxGenerateRetries
    ).genFeatModels()
    if args.dump:
        gFeatGenerator.dump()
