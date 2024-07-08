#!/usr/bin/env python3
"""pycode"""

import asyncio
import time

wait_n = __import__('1-concurrent_coroutines').wait_n


def measure_time(n: int, max_delay: int) -> float:
    """measure_time function"""
    total_time = time.time()
    asyncio.run(wait_n(n, max_delay))
    total_time -= time.time()
    return total_time / -n
