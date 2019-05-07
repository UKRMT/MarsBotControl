import websockets
import asyncio
import json

async def ping():
    async with websockets.connect('ws://localhost:1234') as ws:
        try:
            await ws.send("ping")
        finally:
            await ws.close()


async def work():
    while True:
        await asyncio.sleep(0.5)
        await ping()
        print("Task Executed")

loop = asyncio.get_event_loop()
try:
    asyncio.ensure_future(work())
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    print("Closing Loop")
    loop.close()

