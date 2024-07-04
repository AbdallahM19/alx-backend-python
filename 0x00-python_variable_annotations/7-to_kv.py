#!/usr/bin/env python3
"""py code"""

import typing


def to_kv(k: str, v: typing.Union[int, float]) -> typing.Tuple[str, float]:
    """to_kv function"""
    return (k, v * v)
