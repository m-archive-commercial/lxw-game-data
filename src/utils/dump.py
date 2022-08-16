"""
source: own
author: https://github.com/MarkShawn2020
create: Aug 16, 2022, 17:41
"""
import json
from typing import List

import pandas as pd

from utils.config_path import OUTPUT_DIR, CONFIG_COLUMNS_MAP_PATH
from utils.log import get_logger


logger = get_logger('utils-dump')


def dumpModels(models: List[dict], fn=None):
    df = pd.DataFrame(models)

    # ref: [python - applying a method to a few selected columns in a pandas dataframe - Stack Overflow](https://stackoverflow.com/questions/51306491/applying-a-method-to-a-few-selected-columns-in-a-pandas-dataframe)
    cols_pct = [i for i in list(df.columns) if i.startswith('pct')]
    df[cols_pct] = df[cols_pct].applymap(lambda v: f"{v * 100:05.02f}%")

    # failed
    # [pandas format float decimal places Code Example](https://www.codegrepper.com/code-examples/python/pandas+format+float+decimal+places)
    # pd.set_option('precision', 1)

    with open(CONFIG_COLUMNS_MAP_PATH, "r") as f:
        cols = json.load(f)
    df.rename(columns=cols, inplace=True)
    # reorder cols, ref: https://stackoverflow.com/a/23741480/9422455
    df = df[cols.values()]

    # ref: [python - float64 with pandas to_csv - Stack Overflow](https://stackoverflow.com/questions/12877189/float64-with-pandas-to-csv)
    models_fp_out = OUTPUT_DIR / (fn or 'models.csv')
    df.to_csv(models_fp_out.__str__(), encoding='utf_8', float_format='%.1f')
    logger.info(f'dumped to file://{models_fp_out}')
