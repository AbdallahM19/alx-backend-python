#!/usr/bin/env python3
"""pycode"""

import asyncio
from time import time

async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """measure_runtime function"""
    total_time = time()
    tasks = [async_comprehension() for i in range(4)]
    await asyncio.gather(*tasks)
    total_time = time() - total_time
    return total_time
