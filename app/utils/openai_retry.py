import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from openai import APIError, APITimeoutError


@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((APIError, APITimeoutError, asyncio.TimeoutError)),
)
async def call_with_retry(func, *args, **kwargs):
    """
    Enterprise-grade retry wrapper for OpenAI calls.
    - Max 5 attempts
    - Exponential backoff
    - 60s timeout safety
    """
    return await asyncio.wait_for(func(*args, **kwargs), timeout=60.0)