# -*- coding: utf-8 -*-
"""
@File        : rsa_func.py
@Author      : Aug
@Time        : 2023/1/11 10:00
@Description :
"""
import base64
import rsa


def rsaEncrypt(data):
    """
    encrypt
    data: enciphered data
    """
    (pubkey, privkey) = rsa.newkeys(512)
    content = data.encode("utf-8")
    crypto = rsa.encrypt(content, pubkey)
    return base64.encodebytes(crypto), privkey.save_pkcs1()


def rsaDecrypt(data, privateKey):
    """
    decode
    data: decode data
    """
    pk = rsa.PrivateKey.load_pkcs1(privateKey)
    if type(data) == str:
        data = bytes(data, encoding="utf-8")
    content = rsa.decrypt(base64.decodebytes(data), pk)
    con = content.decode("utf-8")
    return con
