from pathlib import Path
from t.config import json2object
from loguru import logger

logger.add('./log/api/_{time}.log', retention='7 days')

CONF_JSON = str(Path(__file__).resolve().parent.parent) + "/conf/conf.json"

config = json2object(CONF_JSON)

detect_item_path = str(Path(__file__).resolve().parent.parent) + "/conf/detect_item.xlsx"