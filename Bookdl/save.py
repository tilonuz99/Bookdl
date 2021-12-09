from aiofiles import open
from os import path, makedirs
from aiohttp import ClientSession

async def save(file_path, url):
    '''Function to save the file in downloads directory.'''
    async with open(file_path, 'wb') as f:
        try:
            async with ClientSession() as session:
                async with session.get(url) as response:
                    await f.write(await response.read())
                return file_path
        except Exception as e:
            print("File not found!", e)
            return False

