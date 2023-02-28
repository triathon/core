# -*- coding: utf-8 -*-
"""
@File        : detect_item.py
@Author      : Aug
@Time        : 2023/2/25 18:13
@Description :
"""
import xlrd
from xlrd.biffh import XLRDError


def parse_excel(file_path):
    wb = xlrd.open_workbook(file_path)

    try:
        sh = wb.sheet_by_name('data')
    except XLRDError as e:
        return False, e

    result_dict = {}
    for index in range(1, sh.nrows):
        line = sh.row_values(index)
        result_dict[line[1][1:-1]] = {
            "id": line[0],
            "description": line[2].split("](")[0][1:],
            "impact": line[3],
            "confidence": line[4]
        }
    return True, result_dict


if __name__ == '__main__':
    file_path = "D:/project/core/backend/conf/detect_item.xlsx"
    status, res = parse_excel(file_path)

