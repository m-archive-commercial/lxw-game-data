"""
source: own
author: https://github.com/MarkShawn2020
create: Aug 16, 2022, 17:27
"""
import json

import pandas as pd

from utils.config_path import DATA_DIR, OUTPUT_DIR
from utils.log import get_logger

logger = get_logger('utils-regen-users')


def regenerateUsers():
    data_fp_in = DATA_DIR / '精简版数据集.xlsx'
    with open(data_fp_in, "rb") as f:
        df = pd.read_excel(f)

    logger.info(f'read data from file://{data_fp_in}')

    users_fp_out = OUTPUT_DIR / 'users.json'
    with open(users_fp_out, 'w') as f:
        json.dump([dict(j) for i, j in df.iloc[:, 1:].iterrows()], f, ensure_ascii=False, indent=2)

    logger.info(f'regenerated users to file://{users_fp_out}')
