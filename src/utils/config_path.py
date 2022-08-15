"""
source: own
author: https://github.com/MarkShawn2020
create: Aug 15, 2022, 03:11
"""
import os
import sys
import pathlib
from os.path import abspath

# /src/utils/config_path.py
SRC_UTILS_PATH_PATH = pathlib.Path(abspath(__file__))

# /src/utils/
SRC_UTILS_DIR = SRC_UTILS_PATH_PATH.parent

# /src/
SRC_DIR = SRC_UTILS_DIR.parent

# /src/config/
SRC_CONFIG_PATH = SRC_DIR / "config"

# /src/config/columns_map.json
CONFIG_COLUMNS_MAP_PATH = SRC_CONFIG_PATH / "columns_map.json"

# /
PROJECT_DIR = SRC_DIR.parent

# /x/
DATA_DIR = PROJECT_DIR / 'x'
os.makedirs(DATA_DIR, exist_ok=True)

# /output/
OUTPUT_DIR = PROJECT_DIR / 'output'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# /logs/
LOGS_DIR = PROJECT_DIR / "logs"
os.makedirs(LOGS_DIR, exist_ok=True)


