"""
source: own
author: https://github.com/MarkShawn2020
create: Aug 15, 2022, 03:11
"""
import os
import pathlib
from os.path import abspath

SRC_UTILS_PATH_PATH = pathlib.Path(abspath(__file__))
SRC_UTILS_DIR = SRC_UTILS_PATH_PATH.parent
SRC_DIR = SRC_UTILS_DIR.parent
PROJECT_DIR = SRC_DIR.parent

DATA_DIR = PROJECT_DIR / 'data'
os.makedirs(DATA_DIR, exist_ok=True)

OUTPUT_DIR = PROJECT_DIR / 'output'
os.makedirs(OUTPUT_DIR, exist_ok=True)

LOGS_DIR = PROJECT_DIR / "logs"
os.makedirs(LOGS_DIR, exist_ok=True)
