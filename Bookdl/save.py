from aiofiles import open
from os import path, makedirs
from aiohttp import ClientSession

async def save(title, url, parameters):
    '''Function to save the file in downloads directory.'''

    try:
        extension = '.' + parameters['ext']
    except Exception as e:
        logger.debug(e)
        extension = ".pdf"


    file_path =  title + extension

    async with open(file_path, 'wb') as f:
        try:
            async with ClientSession() as session:
                async with session.get(url, params=parameters) as response:
                    await f.write(response.content.read_nowait())
                    total = response.headers.get('Content-Length')
                    size = int(total) / (1024 * 1024)
                    size = round(size, 2)
        except Exception as e:
            print("File not found!", e)
            return

