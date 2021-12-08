from asyncio import run
import re
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from Bookdl.save import save

async def search(book_name):
    '''
    Function to search for related books and save the
    results in books dictionary
    '''
    book = {}
    
    url = "https://www.pdfdrive.com/search?q={}".format(book_name)
    async with ClientSession() as session:
        async with session.get(url) as response:
            source = await response.text()
    soup = BeautifulSoup(source, 'html5lib')
    results = soup.findAll('a', attrs={'class': 'ai-search'})

    for i, result in enumerate(results):
        title = result.find('h2').text
        link = result['href']
        book[i] = (title, link)
    return book

async def download(title, url, ext):
    '''Using selenium driver here to get the download link.'''

    url = "https://www.pdfdrive.com" + url

    async with ClientSession() as session:
        async with session.get(url) as response:
            resp = await response.text()
    soup = BeautifulSoup(resp, 'html5lib')

    bookId = soup.find('button', attrs={'id': 'previewButtonMain'})['data-id']
    session = re.findall(r'session=(.+?)"', str(soup))[0]

    url = "https://www.pdfdrive.com/download.pdf"
    parameters = {'id': bookId, 'h': session, 'ext': ext}
    await save(title, url, parameters)