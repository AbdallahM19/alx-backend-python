#!/usr/bin/env python3
"""pycode"""

import asyncio
from typing import List

async_generator = __import__('0-async_generator').async_generator


async def async_comprehension() -> List[float]:
    """async_comprehension function"""
    result = [i async for i in async_generator()]
    return result
