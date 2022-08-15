"""
source: own
author: https://github.com/MarkShawn2020
create: Aug 14, 2022, 00:36
"""
from __future__ import annotations

import json
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
from utils.config_path import OUTPUT_DIR, CONFIG_COLUMNS_MAP_PATH
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
        logger.debug('generating pre-feats')
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
        except Exception as e:
            logger.debug(e.args)
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
        logger.debug('generating feats')
        predata = self._preGenFeatModel()

        data = dict(
            **predata,
            fStoryTime=self._gen_floats((0, 5, 10, 30, FEAT_STORYTIME_MAX))[0],
            fTutorialTime=self._gen_floats((0, 5, 18, 40, 100))[0],
            fKeepaway=self._gen_floats((0, 5, 60, 100, 200))[0],
            fMoveNum=self._gen_floats((0, 5, 40, 100, 200))[0],

            enumDifficultyLevel=self._gen_choices(FeatDifficultyLevel)[0],
            enumGiftType=self._gen_choices(FeatGiftType)[0],

            isReplayed=self._gen_bools()[0],
            isAcceptGift=self._gen_bools()[0],
            isBug=self._gen_bools()[0],
            isMorePolicy=self._gen_bools()[0],

            pctBadRate=self._gen_percents()[0],
            pctMismatchRate=self._gen_percents()[0],
            pctFeedback=self._gen_percents()[0],
            pctGoodRate=self._gen_percents()[0],
            pctNpcHitRate=self._gen_percents()[0],
            pctGetbackRate=self._gen_percents()[0],
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
                except Exception as e:
                    logger.debug(e.args)
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

        # ref: [python - applying a method to a few selected columns in a pandas dataframe - Stack Overflow](https://stackoverflow.com/questions/51306491/applying-a-method-to-a-few-selected-columns-in-a-pandas-dataframe)
        cols_pct = [i for i in list(df.columns) if i.startswith('pct')]
        df[cols_pct] = df[cols_pct].applymap(lambda v: f"{v * 100:05.02f}%")

        fp = OUTPUT_DIR / (fn or 'feat_models.csv')

        # failed
        # [pandas format float decimal places Code Example](https://www.codegrepper.com/code-examples/python/pandas+format+float+decimal+places)
        # pd.set_option('precision', 1)

        with open(CONFIG_COLUMNS_MAP_PATH, "r") as f:
            cols = json.load(f)
        df.rename(columns=cols, inplace=True)
        # reorder cols, ref: https://stackoverflow.com/a/23741480/9422455
        df = df[cols.values()]

        # ref: [python - float64 with pandas to_csv - Stack Overflow](https://stackoverflow.com/questions/12877189/float64-with-pandas-to-csv)
        df.to_csv(fp.__str__(), encoding='utf_8', float_format='%.1f')
        logger.info(f'dumped to file://{fp}')


if __name__ == '__main__':
    fg = FeatGenerator(solver=PolynomialSolver())
    fg.genFeatModels()
    fg.dump(fn='test.csv')
