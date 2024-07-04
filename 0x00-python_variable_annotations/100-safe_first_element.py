#!/usr/bin/env python3
"""py code"""

from typing import Union, Sequence, List, Any


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """safe_first_element function"""
    if lst:
        return lst[0]
    else:
        return None
