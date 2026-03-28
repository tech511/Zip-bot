import asyncio

queue = asyncio.Queue()

async def worker(process_func):
    while True:
        uid, message = await queue.get()
        try:
            await process_func(uid, message)
        except Exception as e:
            print(e)
        queue.task_done()
