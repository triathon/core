import json
from types import SimpleNamespace as Namespace


def json2object(filename):
    with open(filename) as f:
        data = f.read()
    return json.loads(data, object_hook=lambda d: Namespace(**d))
