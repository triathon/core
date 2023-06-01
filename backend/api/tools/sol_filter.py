# -*- coding: utf-8 -*-
"""
@File        : remove_comment.py
@Author      : JunL
@Time        : 2023/6/1 18:32
@Description :
"""

import re


def remove_comment(solidity_code):
    pattern = r"\/\*[\s\S]*?\*\/"
    code = re.sub(pattern, '', solidity_code, flags=re.MULTILINE)
    print('remove_comment')
    return code
