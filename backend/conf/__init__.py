from pathlib import Path
from t.config import json2object

CONF_JSON = str(Path(__file__).resolve().parent.parent) + "/conf/conf.json"

config = json2object(CONF_JSON)
