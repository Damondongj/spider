import aiohttp
import asyncio
from datetime import datetime

async def fetch(client):
    print("print ClientSession object")
    print(client)
    async with client.get("http://httpbin.org/get") as resp:
        assert resp.status == 200
        return await resp.text() 

async def main():
    async with aiohttp.ClientSession() as client:
        tasks = []
        for i in range(30):
            tasks.append(asyncio.create_task(fetch(client)))
        await asyncio.wait(tasks)
        
loop = asyncio.get_event_loop()

start = datetime.now()

loop.run_until_complete(main())

end = datetime.now()

print("The time spent by the aiohttp version crawler is %s", end - start)


    