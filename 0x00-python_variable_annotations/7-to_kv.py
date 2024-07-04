#!/usr/bin/env python3
"""py code"""

import typing


def to_kv(k: str, v: typing.Union[int, float]) -> tuple:
    """to_kv function"""
    return tuple([k, v * v])
