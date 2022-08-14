"""
source: own
author: https://github.com/MarkShawn2020
create: Aug 14, 2022, 00:36
"""

from typing import List, Type

import numpy as np
import tqdm

from feat_model import FeatModel
from solver.baseSolver import BaseSolver
from solver.polynomialSolver import PolynomialSolver
from utils.ds import ExtendedEnum, FeatDifficultyLevel, FeatGiftType, FeatRealScore
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
        nMaxGenerateRetry=10
    ):
        """

        :param solver:
        :param nTargetModelsEpoch:
        :param nMaxGenerateRetry: tested: when 5, then failed [88/500]
        """
        self._solver = solver
        self.target_models_cnt = nTargetModelsEpoch
        self.maxGenerateTries = nMaxGenerateRetry

        self._feat_models: List[FeatModel] = []

        logger.debug(f'solver: {self._solver}, target_models_cnt: {self.target_models_cnt}')

    def _gen_floats(self, ys):
        return self._solver.fit(ys).generate(self.target_models_cnt)

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
        return np.random.random(self.target_models_cnt) > 0.5

    def _gen_choices(self, choices: Type[ExtendedEnum]):
        """
        :param choices: Type[Enum] need
        :return:
        """
        return np.random.choice(choices, self.target_models_cnt)

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
        assert have_tried < self.maxGenerateTries, f"gen featModel failed for {self.maxGenerateTries} tries"

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

        data = dict(
            **self.preGenFeatModel(),
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


if __name__ == '__main__':
    gSolver: BaseSolver = PolynomialSolver(xdata=[0, 0.25, 0.5, 0.75, 0.97])
    gFeatGenerator = FeatGenerator(gSolver, nMaxGenerateRetry=10)
    failed_cnt = 0
    total_cnt = 500
    for i in tqdm.tqdm(range(total_cnt)):
        try:
            gFeatGenerator.genFeatModel()
        except:
            failed_cnt += 1
    logger.info(f'maxGenerateTries: {gFeatGenerator.maxGenerateTries}, failed: [{failed_cnt}/{total_cnt}]')
