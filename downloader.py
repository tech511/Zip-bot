import asyncio
from config import DOWNLOAD_DIR

semaphore = asyncio.Semaphore(2)

async def download_file(m, uid, i):
    for _ in range(3):
        try:
            async with semaphore:
                return await m.download(
                    file_name=f"{DOWNLOAD_DIR}/{uid}_{i}"
                )
        except:
            await asyncio.sleep(1)
    raise Exception("Download Failed")
