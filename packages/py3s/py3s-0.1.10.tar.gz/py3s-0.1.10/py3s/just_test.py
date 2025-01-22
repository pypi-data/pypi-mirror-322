import asyncio
from dataclasses import dataclass
from enum import Enum
import json
import math
import sys
import time

import httpx
from pyrate_limiter import Duration, Limiter, Rate

from loguru import logger
import requests

async def a(i):
    print(i) 
    await asyncio.sleep(1)

async def main():
    await asyncio.gather(*[a(i) for i in range(10)])

if __name__ == "__main__":
    asyncio.run(main())
