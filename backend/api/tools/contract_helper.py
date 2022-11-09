import json
import re
from collections import OrderedDict
import requests

# 使用contact@triathon.space注册，密码见mainstage项目
# api请求5个/s
apikey = {"bsc": "QVZW45BHPQUXBTNBH7HPZ558C4BM2NAR7P",
          "eth": "22CIFTRV8R4VYDDC3N2YT2QIAYZAJ9Z4T8"}
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


def write_contract(src_code):
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
    code, is_pragma, is_spdx = flatimport(next(iter(sols.values())))
    buffer.append(code)

    return '\n'.join(buffer)
