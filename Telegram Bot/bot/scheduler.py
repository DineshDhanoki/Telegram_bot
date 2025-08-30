import asyncio

class Scheduler:
    def __init__(self, interval_seconds: int):
        self.interval = interval_seconds

    async def run_forever(self, coro_fn):
        while True:
            try:
                await coro_fn()
            except Exception as e:
                print("[scheduler] error:", e)
            await asyncio.sleep(self.interval)
