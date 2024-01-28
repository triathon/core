import json
import re
from collections import OrderedDict
import requests
from conf import config

# register using contact@triathon.space ，see the “mainstage” project for passwords
# api request 5/s
apikey = {"bsc": config.apikey_bsc,
          "eth": config.apikey_eth}
endpoint = {"bsc": "https://api.bscscan.com/api",
            "eth": "https://api.etherscan.io/api"}

ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
headers = {"user-agent": ua}
session = requests.session()


def fetch_contract_meta(network, address):
    """
    Obtaining contract Data
    :param network:
    :param address:
    :return:
    """
    params = {"module": "contract",
              "action": "getsourcecode",
              "address": address,
              "apikey": apikey[network],
              }
    rst = session.get(endpoint[network], params=params, headers=headers).json()
    if int(rst['status']) == 1:
        return rst['result'][0]


def write_contract(file_name, src_code):
    """
    Merge network multi-file code
    :param src_code:
    :return:
    """
    sols_ = json.loads(src_code[1:-1], object_pairs_hook=OrderedDict)['sources']

    sols = OrderedDict()
    for k, v in sols_.items():
        k = k.split("/")[-1]
        sols[k] = v

    has_flat = set()

    def flatimport(filecontent, is_pragma_=False, is_spdx_=False):
        _buffer = []
        for line in filecontent['content'].split("\n"):
            if "pragma" in line[:6]:
                if is_pragma_ is False:
                    is_pragma_ = True
                    _buffer.append(line)
                continue

            elif "SPDX-License-Identifier" in line:
                if is_spdx_ is False:
                    is_spdx_ = True
                    _buffer.append(line)
                continue

            elif line[:6] == 'import':
                re_import_ = re.search('import +"(.*)";', line)
                if not re_import_:
                    re_import_ = re.search("import +'(.*)';", line)
                import_file_ = (re_import_[1]).split("/")[-1]
                # Verify whether files are merged
                if import_file_ not in has_flat:
                    has_flat.add(import_file_)
                    code_, is_pragma_, is_spdx_ = flatimport(sols[import_file_], is_pragma_, is_spdx_)
                    _buffer.append(code_)
                continue
            _buffer.append(line)
        return '\n'.join(_buffer), is_pragma_, is_spdx_

    buffer = []
    first_file = sols.get(file_name+".sol")
    if not first_file:
        first_file = next(iter(sols.values()))
    code, is_pragma, is_spdx = flatimport(first_file)
    buffer.append(code)

    return '\n'.join(buffer)
