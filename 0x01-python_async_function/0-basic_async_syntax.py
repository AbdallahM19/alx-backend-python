#!/usr/bin/env python3
"""pycode"""

import asyncio
import random


async def wait_random(max_delay: int = 10) -> float:
    """wait_random function"""
    sleep_time = random.uniform(0, max_delay)
    await asyncio.sleep(sleep_time)
    return sleep_time
