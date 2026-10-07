import asyncio


class SimulatedTransformer:
    def __init__(self, latency_seconds: float, max_concurrency: int) -> None:
        self._latency_seconds = latency_seconds
        self._semaphore = asyncio.Semaphore(max_concurrency)

    async def transform(self, text: str) -> str:
        async with self._semaphore:
            await asyncio.sleep(self._latency_seconds)
        return text.upper()
