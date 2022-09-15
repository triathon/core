import time
import requests
from bs4 import BeautifulSoup
from ..models.module import Testing


eth_code_url = r'https://etherscan.io/address/'
bsc_code_url = r'https://bscscan.com/address/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 '
                  'Safari/537.36 '
}


def print_time():
    print(time.strftime("%Y-%m-%d %H:%M:%S:", time.localtime()), end=' ')
    return 0


def getCode(address, s_type):
    global page
    s_url = eth_code_url + address + "#code"
    if s_type != "eth":
        s_url = bsc_code_url + address + "#code"

    failedTimes = 100
    while True:
        if failedTimes <= 0:
            print_time()
            return "Too many failures, check the network environment！"

        failedTimes -= 1
        try:
            print_time()
            page = requests.get(s_url, headers=headers, timeout=10)
            break

        except requests.exceptions.ConnectionError:
            print_time()
            print('ConnectionError！Please wait 3 seconds！')
            time.sleep(3)

        except requests.exceptions.ChunkedEncodingError:
            print_time()
            print('ChunkedEncodingError！Please wait 3 seconds！')
            time.sleep(3)

        except EOFError:
            print_time()
            print('unknown error！Please wait 3 seconds！')
            time.sleep(3)

    page.encoding = page.apparent_encoding
    soup = BeautifulSoup(page.text, "html.parser")
    targetPRE = soup.find_all('pre', 'js-sourcecopyarea editor')
    if targetPRE:
        return targetPRE[0].text


def get_contract(address, s_type, user_id, db=True):
    storage = 0
    if not address or not s_type or s_type not in ["eth", "bsc"]:
        return "No valid type specified"
    data = getCode(address, s_type)
    if not data:
        return False, "No valid contract detected"
    if db:
        storage_data = Testing.create(
            content=data,
            user_id=user_id
        )
        storage = storage_data.id
    return True, data, storage
