"""
source: own
author: https://github.com/MarkShawn2020
create: Aug 14, 2022, 00:36
"""
from __future__ import annotations

from typing import List

from pydantic import ValidationError

from src.feat_model import FeatModel


class FeatGenerator:

    def __init__(self, target_models_count=500):
        self._feat_models: List[FeatModel] = []

    def genFeatModel(self, have_tried=0, max_tries=5) -> FeatModel:
        assert have_tried < max_tries, f"gen featModel failed for {max_tries} tries"
        try:
            feat_model = FeatModel(
                storyTime=0.,
                tutorialTime=0.,
                duration=0,
                score=0.,
                difficultyLevel=0,
                replayTimes=0,
                hitRate=0.,
                badRate=0.,
                mismatchRate=0.,
                keepaway=0.,
                feedback=0.,
                goodRate=0.,
                moveNum=0.,
                clickRate=0.,
                npcHitRate=0.,
                getbackRate=0.,
                isAcceptGift=0,
                giftType=0,
                isUpload=0,
                isRealScore=-1,
                bugTimes=0,
                batteryTimes=0,
                filterLenTimes=0,
                signalTimes=0,
                impulseTimes=0,
                morePolicy=0,
                lifetime=0,
            )
            self._feat_models.append(feat_model)
            return feat_model
        except ValidationError:
            return self.genFeatModel(have_tried + 1, max_tries)
