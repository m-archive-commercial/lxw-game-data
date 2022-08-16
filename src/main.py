"""
source: own
author: https://github.com/MarkShawn2020
create: Aug 15, 2022, 16:09
"""
import argparse
import json

import numpy as np
import pandas as pd
from tqdm import tqdm

from feat_generator import FeatGenerator
from solver.baseSolver import BaseSolver
from solver.linearSmoothSolver import LinearSmoothSolver
from utils.config_path import OUTPUT_USERS_DATA_PATH, OUTPUT_MODELS_DATA_PATH
from utils.dump import dumpModels
from utils.log import get_logger
from utils.regeneate_users import regenerateUsers

logger = get_logger('MAIN')

with open(OUTPUT_USERS_DATA_PATH, 'r') as f:
    users = json.load(f)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--no-regen-users',
        help='regenerate users data from xlsx to json',
        action='store_true'
    )

    parser.add_argument(
        '--no-dump',
        help='dump the feature models to file',
        action='store_true',
    )

    parser.add_argument(
        '--users-cnt',
        help='users to generate',
        default=50,
        type=int,
    )

    parser.add_argument(
        '--user-times',
        help='run times of each user',
        default=10,
        type=int,
    )

    parser.add_argument(
        '--perturbation',
        help='perturbation based on the target value, range: (0, 1), 0: always target; 1: always random',
        default=0.3,
        type=float,
    )

    parser.add_argument(
        '--main-space',
        help='decides the main space based on center on domain; range: (0,1); 0: normal, 1: always center',
        default=.8,
        type=float,
    )

    parser.add_argument(
        '--nMaxGenRetries',
        help='number of retrying to generate models in each epoch, recommending 5-10',
        default=10,
        type=int,
    )

    args = parser.parse_args()
    logger.info(args)

    if not args.no_regen_users:
        regenerateUsers()

    gSolver: BaseSolver = LinearSmoothSolver() \
        .setMainSpace(args.main_space)

    gModels = []
    selects = np.random.choice(range(len(users)), args.users_cnt, replace=False)
    for user_i, selected_num in enumerate(tqdm(selects)):
        logger.debug(f'[User #{user_i + 1}] generating the {selected_num}th user...')
        user = users[selected_num]
        gFeatGenerator = FeatGenerator(gSolver, nMaxGenRetries=args.nMaxGenRetries) \
            .setPerturbation(args.perturbation) \
            .setUser(user)
        for i in range(args.user_times):
            gModel = gFeatGenerator.genModel()
            gModels.append(gModel)

    logger.info(f'done generating all the {args.users_cnt} users with {len(gModels)} models')

    if not args.no_dump:
        dumpModels(gModels)
