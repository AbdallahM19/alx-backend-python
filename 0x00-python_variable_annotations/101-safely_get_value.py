#!/usr/bin/env python3
"""py code"""

from typing import Union, Any, Mapping, TypeVar


T = TypeVar('T')
defa = Union[T, None]
res = Union[Any, T]


def safely_get_value(dct: Mapping, key: Any, default: defa = None) -> res:
    """safely_get_value function"""
    if key in dct:
        return dct[key]
    else:
        return default
