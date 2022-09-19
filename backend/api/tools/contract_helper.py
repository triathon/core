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
    params = {"module": "contract",
              "action": "getsourcecode",
              "address": address,
              "apikey": apikey[network],
              }
    rst = session.get(endpoint[network], params=params, headers=headers).json()
    if int(rst['status']) == 1:
        return rst['result'][0]

# get_contract_source_code("bsc", "0x6EcF4F241Cb0bC3455821F69CA9bDC7B0E1e0C57")
# print(fetch_contract_meta("eth", "0xdAC17F958D2ee523a2206206994597C13D831ec7"))
