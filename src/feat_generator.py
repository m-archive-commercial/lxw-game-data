"""
source: own
author: https://github.com/MarkShawn2020
create: Aug 14, 2022, 00:36
"""
from __future__ import annotations

import json
from enum import Enum
from typing import List, Type

import numpy as np
import pandas as pd
import tqdm

from config.feats import FEAT_STORYTIME_MAX, FEAT_SIGNALTIMES_MAX, FEAT_FILTERLENTIMES_MAX, FEAT_BATTERYTIMES_MAX, \
    FEAT_IMPULSETIMES_MAX
from config.model import DEFAULT_NUM_MODELS_TO_GEN
from ds import ExtendedEnum, FeatDifficultyLevel, FeatGiftType, FeatRealScore
from feat_model import FeatModel
from solver.baseSolver import BaseSolver
from solver.linearSmoothSolver import LinearSmoothSolver
from utils.config_path import OUTPUT_DIR, CONFIG_COLUMNS_MAP_PATH, USERS_DATA_PATH
from utils.log import get_logger
from utils.regenerate_field import regenerate
from utils.validator_feats import validateHitRate, validateImpulseTimes, validateLifetime

logger = get_logger('FeatGenerator')

with open(CONFIG_COLUMNS_MAP_PATH, 'r') as f:
    colsMap = json.load(f)


class FeatGenerator:

    def __init__(
        self,
        solver: BaseSolver,
        nModelsToGen=DEFAULT_NUM_MODELS_TO_GEN,
        nModelsEpoch=1,
        nMaxGenRetries=10,
    ):
        """

        :param nModelsEpoch:
        :param nMaxGenRetries: tested: when 5, then failed [88/500]
        """
        self._solver = solver
        self._nModelsToGen = nModelsToGen
        self._nModelsEpoch = nModelsEpoch
        self._nMaxGenRetries = nMaxGenRetries

        self._perturbation = 0
        self._user = None

        self._feat_models: List[FeatModel] = []

    def setPerturbation(self, v):
        self._perturbation = v
        return self

    def setUser(self, user):
        self._user = user
        return self

    def _genFloats(self, ys, xs=None, target=None, ):
        if xs:
            self._solver.setXdata(xs)
        result = self._solver.setYdata(ys).fit().generate(self._nModelsEpoch)
        if target and self._user is not None:
            """
            扰动为0 --> 全部为目标值
            扰动为1 --> 全部为随机值
            """
            result = self._perturbation * result + (1 - self._perturbation) * target
        return result

    def _genInts(self, ys, xs=None, target=None, ):
        """
        tip: here we can use .astype(int) since we didn't use the `StrictInt`
        :param ys:
        :return:
        """
        result = self._genFloats(ys, xs).astype(int)
        if target and self._user is not None:
            result = np.round(self._perturbation * result + (1 - self._perturbation) * target).astype(int)
        return result

    def _genBools(self, target=None):
        result = np.random.random(self._nModelsEpoch) > 0.5
        if target and self._user is not None:
            result = np.round(self._perturbation * result + (1 - self._perturbation) * target)
        return result

    def _gen_choices(self, choices: Type[ExtendedEnum], target=None):
        """
        :param choices: Type[Enum] need
        :return:
        """
        result = np.random.choice(choices, self._nModelsEpoch)
        if target and self._user is not None:
            result = np.round(self._perturbation * result + (1 - self._perturbation) * target)
        return result

    def _genFeatOfLifetime(self, batteryTimes):
        """
        need to be manually aligned
        todo: add the `target` benchmark
        :return:
        """
        if batteryTimes > 0:
            return 60 + batteryTimes * 30
        return regenerate(
            lambda: self._genInts(60),
            lambda v: True
        )

    def _genFeatOfRealScore(self, isUpload):
        if isUpload == 0:
            return FeatRealScore.NO_DATA
        return self._gen_choices(FeatRealScore, target=self._getUserFeat('enumRealScore'))[0]

    def _getUserFeat(self, varName):
        return None if self._user is None else self._user[colsMap[varName]]

    def _genPreModel(self, have_tried=0):
        """
        fScore --> pctHitRate
        fScore, intClickFreq, isDuration, intBatteryTimes --> intLifetime
        intBatteryTimes, intFilterLenTimes, intSignalTimes --> intImpulseTimes
        """
        logger.debug('generating pre-feats')
        assert have_tried < self._nMaxGenRetries, f"gen featModel failed for {self._nMaxGenRetries} tries"

        fScore = self._genFloats((0, 5, 40, 100, 200), target=self._getUserFeat('fScore'))[0]
        pctHitRate = self._genFloats(
            (0, .1, .5, .9, 1),
            # hitRate应该保证80%的数据结果都在50%以上
            xs=(0, .1, .2, .5, 1),
            target=self._getUserFeat('pctHitRate'))[0]

        intBatteryTimes = self._genInts(
            (0, 0, 2, 5, FEAT_BATTERYTIMES_MAX),
            target=self._getUserFeat('intBatteryTimes')
        )[0]
        intFilterLenTimes = self._genInts(
            (0, 1, 2, 5, FEAT_FILTERLENTIMES_MAX),
            target=self._getUserFeat('intFilterLenTimes')
        )[0]
        intSignalTimes = self._genInts(
            (0, 1, 2, 5, FEAT_SIGNALTIMES_MAX),
            target=self._getUserFeat('intSignalTimes')
        )[0]
        intImpulseTimes = self._genInts(
            (0, 1, 2, 5, FEAT_IMPULSETIMES_MAX),
            target=self._getUserFeat('intImpulseTimes')
        )[0]

        intClickFreq = self._genInts((0, 100, 830, 2000, 3000),
            target=self._getUserFeat('intClickFreq'))[0]
        isDuration = self._genBools(target=self._getUserFeat('isDuration'))[0]
        intLifetime = self._genFeatOfLifetime(intBatteryTimes)

        isUpload = self._genBools(target=self._getUserFeat('isUpload'))[0]
        enumRealScore = self._genFeatOfRealScore(isUpload)

        try:
            validateHitRate(pctHitRate, {'fScore': fScore})
            validateImpulseTimes(intImpulseTimes, {
                "intBatteryTimes"  : intBatteryTimes,
                "intFilterLenTimes": intFilterLenTimes,
                "intSignalTimes"   : intSignalTimes
            })
            validateLifetime(intLifetime, {
                "fScore"         : fScore,
                "intClickFreq"   : intClickFreq,
                "isDuration"     : isDuration,
                "intBatteryTimes": intBatteryTimes
            })
        except Exception as e:
            logger.debug(e.args)
            return self._genPreModel(have_tried + 1)
        else:
            return {
                "fScore"           : fScore,
                "pctHitRate"       : pctHitRate,
                "intBatteryTimes"  : intBatteryTimes,
                "intFilterLenTimes": intFilterLenTimes,
                "intSignalTimes"   : intSignalTimes,
                "intImpulseTimes"  : intImpulseTimes,
                "intClickFreq"     : intClickFreq,
                "isDuration"       : isDuration,
                "intLifetime"      : intLifetime,
                "isUpload"         : isUpload,
                "enumRealScore"    : enumRealScore,
            }

    def genModel(self) -> dict:
        logger.debug('generating feats')
        preModel = self._genPreModel()

        data = dict(
            **preModel,
            fStoryTime=self._genFloats((0, 5, 10, 30, FEAT_STORYTIME_MAX), target=self._getUserFeat('fStoryTime'))[0],
            fTutorialTime=self._genFloats((0, 5, 18, 40, 100), target=self._getUserFeat('fTutorialTime'))[0],
            fKeepaway=self._genFloats((0, 5, 60, 100, 200), target=self._getUserFeat('fKeepaway'))[0],
            fMoveNum=self._genFloats((0, 5, 40, 100, 200), target=self._getUserFeat('fMoveNum'))[0],

            enumDifficultyLevel=self._gen_choices(FeatDifficultyLevel, target=self._getUserFeat('enumDifficultyLevel'))[
                0],
            enumGiftType=self._gen_choices(FeatGiftType, target=self._getUserFeat('enumGiftType'))[0],

            isReplayed=self._genBools(target=self._getUserFeat('isReplayed'))[0],
            isAcceptGift=self._genBools(target=self._getUserFeat('isAcceptGift'))[0],
            isBug=self._genBools(target=self._getUserFeat('isBug'))[0],
            isMorePolicy=self._genBools(target=self._getUserFeat('isMorePolicy'))[0],

            pctBadRate=self._genFloats(
                # badRate值域改成0-70%吧
                [0, .1, .3, .5, .7],
                target=self._getUserFeat('pctBadRate')
            )[0],
            pctMismatchRate=self._genFloats(
                # mismatchRate 应该保证80%的数据结果都在20%以下
                [0, .05, .1, .2, 1],
                xs=[0, .1, .5, .8, 1],
                target=self._getUserFeat('pctMismatchRate'),
            )[0],
            pctFeedback=self._genFloats([0, .1, .5, .9, 1], target=self._getUserFeat('pctFeedback'))[0],
            pctGoodRate=self._genFloats([0, .1, .5, .9, 1], target=self._getUserFeat('pctGoodRate'))[0],
            floatNpcHitRate=self._genFloats(
                [0, 1, 3, 5, 10],
                target=self._getUserFeat('floatNpcHitRate'),
            )[0],
            pctGetbackRate=self._genFloats(
                # getbackRate 应该保证80%的数据结果都在50%以下
                [0, .1, .3, .5, .1],
                xs=[0, .1, .5, .8, 1],
                target=self._getUserFeat('pctGetbackRate'),
            )[0],
        )
        model = FeatModel(**data)
        self._feat_models.append(model)
        logger.debug(f'generated feat gModel: {model}')
        result = dict(**self._user)
        for k, v in model.dict().items():
            try:
                k = self._getUserFeat(k)
            except KeyError:
                logger.debug(f'not found key in user data inputted(from excel): {k}')
            finally:
                result[k] = v
        return result

    def genFeatModels(self) -> List[dict]:
        total_tries = 0
        failed_tries = 0
        results = []
        for _ in tqdm.tqdm(range(self._nModelsToGen)):
            while True:
                try:
                    total_tries += 1
                    results.append(self.genModel())
                except Exception as e:
                    logger.debug(e.args)
                    failed_tries += 1
                else:
                    break
        logger.info({
            "config": {
                "target models": self._nModelsToGen,
                "max retries"  : self._nMaxGenRetries,
            },
            "tries" : {
                "failed": failed_tries,
                "total" : total_tries
            }
        })
        return results

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
    class Mode(str, Enum):
        GEN_SINGLE_MODEL = "gen-single-gModel"
        GEN_AND_DUMP_ALL = "gen-and-dump-all"

    mode = Mode.GEN_SINGLE_MODEL

    gSolver = LinearSmoothSolver() \
        .setPeakRatio(.3) \
        .setMainSpace(.8)

    with open(USERS_DATA_PATH, 'r') as f:
        users = json.load(f)
    fg = FeatGenerator(solver=gSolver) \
        .setUser(users[0]) \
        .setPerturbation(.3)

    if mode == Mode.GEN_AND_DUMP_ALL:
        fg.genFeatModels()
        fg.dump(fn='test.csv')

    elif mode == Mode.GEN_SINGLE_MODEL:
        gModels = [fg.genModel() for i in range(10)]
        logger.info(gModels)
