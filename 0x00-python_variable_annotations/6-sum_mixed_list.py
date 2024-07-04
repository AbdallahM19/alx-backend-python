#!/usr/bin/env python3
"""py code"""

import typing


def sum_mixed_list(mxd_lst: typing.List[typing.Union[int, float]]) -> float:
    """sum_mixed_list function"""
    sum_list = 0.00
    for i in mxd_lst:
        sum_list += i
    return float(sum_list)
