"""
source: own
author: https://github.com/MarkShawn2020
create: Aug 14, 2022, 00:36
"""

from typing import List, Iterator, Type

import numpy as np
from pydantic import ValidationError

from algo.fit import fit_and_gen
from feat_model import FeatModel, FeatGiftType, FeatDifficultyLevel, ExtendedEnum
from log import get_logger
from utils import battery2LifeTime, upload2score

logger = get_logger('FeatGenerator')


class FeatGenerator:

    def __init__(
        self,
        xs: Iterator[float] = None,
        sigma: Iterator[float] = None,
        target_models_count=500,
    ):
        # since we couldn't control the right hand strictly limited to 1,
        # we decreased 1 to be a bit smaller
        if xs is None:
            xs = (0, 0.25, 0.5, 0.75, 0.95)
        if sigma is None:
            sigma = (0.01, 1, 0.1, 1, 0.01)
        self._feat_models: List[FeatModel] = []
        self._xs = xs
        self._sigma = sigma
        self._N = target_models_count

        logger.info({'xs': self._xs, 'sigma': self._sigma, 'N': self._N})

    def _gen_floats(self, ys):
        return fit_and_gen(self._xs, ys, sigma=self._sigma, N=self._N)

    def _gen_ints(self, ys):
        """
        TODO: can not use .astype(int)
        :param ys:
        :return:
        """
        return self._gen_floats(ys).astype(int)

    def _gen_percents(self):
        return self._gen_floats(self._xs)

    def _gen_bools(self):
        return np.random.random(self._N) > 0.5

    def _gen_choices(self, choices: Type[ExtendedEnum]):
        """

        :param choices: Type[Enum] need
        :return:
        """
        return np.random.choice(choices.values(), self._N)

    # TODO: generate multiple each period
    def genFeatModel(self, have_tried=0, max_tries=5) -> FeatModel:
        assert have_tried < max_tries, f"gen featModel failed for {max_tries} tries"
        try:
            batteryTimes = self._gen_ints((0, 0, 2, 5, 20))
            lifeTimes = battery2LifeTime(batteryTimes)
            isUpload = self._gen_bools()
            isRealScore = upload2score(isUpload)

            data = dict(
                storyTime=self._gen_floats((0, 5, 10, 30, 100))[0],
                tutorialTime=self._gen_floats((0, 5, 18, 40, 100))[0],
                duration=self._gen_bools()[0],
                score=self._gen_floats((0, 5, 40, 100, 200))[0],
                difficultyLevel=self._gen_choices(FeatDifficultyLevel)[0],
                replayTimes=self._gen_bools()[0],
                # TODO: percents distribution function ?
                hitRate=self._gen_percents()[0],
                badRate=self._gen_percents()[0],
                mismatchRate=self._gen_percents()[0],
                keepaway=self._gen_floats((0, 5, 60, 100, 200))[0],
                feedback=self._gen_percents()[0],
                goodRate=self._gen_percents()[0],
                moveNum=self._gen_floats((0, 5, 40, 100, 200))[0],
                clickRate=self._gen_floats((0, 100, 830, 2000, 3000))[0],
                npcHitRate=self._gen_percents()[0],
                getbackRate=self._gen_percents()[0],
                isAcceptGift=self._gen_bools()[0],
                giftType=self._gen_choices(FeatGiftType)[0],
                isUpload=isUpload[0],
                isRealScore=isRealScore[0],
                bugTimes=self._gen_bools()[0],
                batteryTimes=batteryTimes[0],
                filterLenTimes=self._gen_ints((0, 1, 2, 5, 20))[0],
                signalTimes=self._gen_ints((0, 1, 2, 5, 20))[0],
                impulseTimes=self._gen_ints((0, 1, 2, 5, 20))[0],
                morePolicy=self._gen_bools()[0],
                lifetime=lifeTimes[0]
            )
            # logger.info(f'data: {data}')
            feat_model = FeatModel(**data)
            self._feat_models.append(feat_model)
            logger.info(f'√ generated: {feat_model}')
            return feat_model

        except (ValidationError, RuntimeError) as e:
            have_tried += 1
            logger.warning(f'x [#{have_tried}] failed to generate, reason: {e}')
            return self.genFeatModel(have_tried, max_tries)


if __name__ == '__main__':
    feat_generator = FeatGenerator()
    feat_generator.genFeatModel(max_tries=5)
