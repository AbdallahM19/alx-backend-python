#!/usr/bin/env python3
"""py code"""

import typing


def sum_list(input_list: typing.List[float]) -> float:
    """sum_list function"""
    sum_list = 0.00
    for i in input_list:
        sum_list += i
    return float(sum_list)
