"""
source: own
author: https://github.com/MarkShawn2020
create: Aug 14, 2022, 00:36
"""
from __future__ import annotations

from typing import List, Type

import numpy as np
import pandas as pd
import tqdm

from config.feats import FEAT_STORYTIME_MAX
from config.model import DEFAULT_NUM_MODELS_TO_GEN
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
        nModelsToGen=DEFAULT_NUM_MODELS_TO_GEN,
        nModelsEpoch=1,
        nMaxGenRetries=10
    ):
        """

        :param nModelsEpoch:
        :param nMaxGenRetries: tested: when 5, then failed [88/500]
        """
        self._solver = solver
        self.nModelsToGen = nModelsToGen
        self.nModelsEpoch = nModelsEpoch
        self.nMaxGenRetries = nMaxGenRetries

        self._feat_models: List[FeatModel] = []

    def _gen_floats(self, ys, xs=None):
        if xs:
            self._solver.initX(xs)
        return self._solver.initY(ys).fit().generate(self.nModelsEpoch)

    def _gen_ints(self, ys, xs=None):
        """
        tip: here we can use .astype(int) since we didn't use the `StrictInt`
        :param ys:
        :return:
        """
        return self._gen_floats(ys, xs).astype(int)

    def _gen_percents(self, xs=None):
        """
        percent can be generated linearly, which is the same args like `xdata`
        :return:
        """
        return self._gen_floats(self._solver.xdata, xs)

    def _gen_bools(self):
        return np.random.random(self.nModelsEpoch) > 0.5

    def _gen_choices(self, choices: Type[ExtendedEnum]):
        """
        :param choices: Type[Enum] need
        :return:
        """
        return np.random.choice(choices, self.nModelsEpoch)

    def _genFeatOfLifetime(self, batteryTimes):
        """
        need to be manually aligned
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

    def _preGenFeatModel(self, have_tried=0):
        """
        fScore --> pctHitRate
        fScore, intClickFreq, isDuration, intBatteryTimes --> intLifetime
        intBatteryTimes, intFilterLenTimes, intSignalTimes --> intImpulseTimes
        """
        assert have_tried < self.nMaxGenRetries, f"gen featModel failed for {self.nMaxGenRetries} tries"

        score = self._gen_floats((0, 5, 40, 100, 200))[0]
        hitRate = self._gen_percents()[0]

        batteryTimes = self._gen_ints((0, 0, 2, 5, 20))[0]
        filterLenTimes = self._gen_ints((0, 1, 2, 5, 20))[0]
        signalTimes = self._gen_ints((0, 1, 2, 5, 20))[0]
        impulseTimes = self._gen_ints((0, 1, 2, 5, 20))[0]

        clickRate = self._gen_ints((0, 100, 830, 2000, 3000))[0]
        duration = self._gen_bools()[0]
        lifetime = self._genFeatOfLifetime(batteryTimes)

        isUpload = self._gen_bools()[0]
        realScore = self._genFeatOfRealScore(isUpload)

        try:
            validateHitRate(hitRate, {'fScore': score})
            validateImpulseTimes(impulseTimes, {
                "intBatteryTimes"  : batteryTimes,
                "intFilterLenTimes": filterLenTimes,
                "intSignalTimes"   : signalTimes
            })
            validateLifetime(lifetime, {
                "fScore"         : score,
                "intClickFreq"   : clickRate,
                "isDuration"     : duration,
                "intBatteryTimes": batteryTimes
            })
        except:
            return self._preGenFeatModel(have_tried + 1)
        else:
            return {
                "fScore"           : score,
                "pctHitRate"       : hitRate,
                "intBatteryTimes"  : batteryTimes,
                "intFilterLenTimes": filterLenTimes,
                "intSignalTimes"   : signalTimes,
                "intImpulseTimes"  : impulseTimes,
                "intClickFreq"     : clickRate,
                "isDuration"       : duration,
                "intLifetime"      : lifetime,
                "isUpload"         : isUpload,
                "enumRealScore"    : realScore,
            }

    def genFeatModel(self) -> FeatModel:

        predata = self._preGenFeatModel()

        data = dict(
            **predata,
            storyTime=self._gen_floats((0, 5, 10, 30, FEAT_STORYTIME_MAX))[0],
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
        for _ in tqdm.tqdm(range(self.nModelsToGen)):
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
                "target models": self.nModelsToGen,
                "max retries"  : self.nMaxGenRetries,
            },
            "tries" : {
                "failed": failed_tries,
                "total" : total_tries
            }
        })
        return self

    def dump(self, fn=None):
        df = pd.DataFrame([dict(i) for i in self._feat_models])

        df_pcts = df.loc[[i.startswith('pct') for i in df.columns]]
        df_pcts = df_pcts.apply(lambda v: f"{round(v * 100, 2)}%")
        fp = OUTPUT_DIR / (fn or 'feat_models.csv')
        df.to_csv(fp.__str__(), encoding='utf_8', )
        logger.info(f'dumped to file://{fp}')


if __name__ == '__main__':
    fg = FeatGenerator(solver=PolynomialSolver())
    fg.genFeatModels()
    fg.dump(fn='test.csv')
