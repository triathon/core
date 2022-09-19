from eth_account.messages import encode_defunct
from web3.auto import w3

nonce = "351794"
private_key = ''
msg = encode_defunct(text=f'Welcome login with nonce={nonce}')
sign = w3.eth.account.sign_message(msg, private_key)
print(sign.signature.hex())
