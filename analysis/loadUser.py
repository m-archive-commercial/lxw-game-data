"""
source: own
author: https://github.com/MarkShawn2020
create: Aug 16, 2022, 09:16
"""
import json

import numpy as np
import pandas as pd

from utils.config_path import DATA_DIR, OUTPUT_DIR

with open(DATA_DIR / '精简版数据集.xlsx', "rb") as f:
    df = pd.read_excel(f)

# selectedRows = np.random.choice(range(df.shape[0]), 50,
#     replace=False,  # ensure unique
# )
# df = df.iloc[selectedRows]

with open(OUTPUT_DIR / 'users.json', 'w') as f:
    json.dump([dict(j) for i, j in df.iloc[:, 1:].iterrows()], f, ensure_ascii=False, indent=2)
