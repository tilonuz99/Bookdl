from asyncio import run
from re import findall
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
            source = await response.read()
    soup = BeautifulSoup(source, 'html.parser', from_encoding="utf-8")
    # found_count = soup.findAll("div", attrs={'id': "result-found"})
    # print(found_count)
    results = soup.findAll('a', attrs={'class': 'ai-search'})

    for i, result in enumerate(results):
        title = result.find('h2').text
        link = result['href']

        book[i] = (title, link)
    return book


async def genereate_url(url):
    url = "https://www.pdfdrive.com" + url

    async with ClientSession() as session:
        async with session.get(url) as response:
            resp = await response.read()
    soup = BeautifulSoup(resp, 'html.parser')

    file_info = soup.find('div', attrs={'class': 'ebook-file-info'})
    info = [x.get_text() for x in file_info.findAll('span', attrs={'class': 'info-green'})]

    bookId = soup.find('button', attrs={'id': 'previewButtonMain'})['data-id']
    session = findall(r'session=(.+?)"', str(soup))[0]

    url = "https://www.pdfdrive.com/download.pdf?"
    return f"{url}id={bookId}&h={session}&ext=pdf", info