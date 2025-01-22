"""
Make config file here.

Thisi file is to store programming config.
"""

import ast
import logging
import os
import pathlib

DEBUG = ast.literal_eval(os.getenv("CORE_DEBUG", "False"))

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formmater = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

fh = logging.FileHandler("info.log")
fh.setLevel(logging.INFO)
fh.setFormatter(formmater)

sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
sh.setFormatter(formmater)

if not DEBUG:
    logger.addHandler(fh)


# generate project root.
project_root = pathlib.Path(__file__).parent.parent.parent

csv_folder = "additional_data_for_material"

udl2_file_keys = [
    "Record Type",
    "Date/Time(中国标准时间)",
    "Potential DC Reading",
    "Potential DC Units",
    "Potential DC Instant Off Reading",
    "Potential DC Instant Off Units",
    "Potential AC Reading",
    "Potential AC Units",
    "Current DC Reading",
    "Current DC Units",
    "Current AC Reading",
    "Current AC Units",
]
