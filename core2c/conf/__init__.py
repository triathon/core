# -*- coding: utf-8 -*-
"""
@File        : __init__.py
@Author      : Aug
@Time        : 2023/2/13 15:54
@Description :
"""
import json
import os
from pathlib import Path
from loguru import logger

logger.add('./log/api/_{time}.log', retention='7 days')

CONF_JSON = str(Path(__file__).resolve().parent.parent) + "/conf/"

with open(os.path.join(CONF_JSON, 'conf.json')) as f:
    config = json.loads(f.read())
