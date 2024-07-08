#!/usr/bin/env python3
"""pycode"""

import asyncio
from typing import List

wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """wait_n function"""
    sleep_time_list = []
    for _ in range(n):
        sleep_time_list.append(wait_random(max_delay))
    tasks_list = [await x for x in asyncio.as_completed(sleep_time_list)]
    return tasks_list
