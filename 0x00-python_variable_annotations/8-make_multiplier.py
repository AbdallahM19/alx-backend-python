#!/usr/bin/env python3
"""py code"""

import typing


def make_multiplier(multiplier: float) -> typing.Callable[[float], float]:
    """make_multiplier function"""
    def multiplier_func(num):
        return multiplier * num
    return multiplier_func
