#!/usr/bin/env python3
"""pycode"""

import asyncio
from typing import List

task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """wait_n function"""
    sleep_time_list = []
    for _ in range(n):
        sleep_time_list.append(task_wait_random(max_delay))
    return [await x for x in asyncio.as_completed(sleep_time_list)]
