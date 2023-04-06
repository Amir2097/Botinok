import httpx
from bs4 import BeautifulSoup


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Referer': 'https://horo.mail.ru/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
}


async def get_responce(link: str):
    async with httpx.AsyncClient(headers=headers, follow_redirects=True) as htx:
        result: httpx.Response = await htx.get(url=link)
        if result.status_code != 200:
            return f'Что-то не так!'
        else:
            return await result.aread()


async def get_zodiac(zodiac: str):
    url = f'https://horo.mail.ru/prediction/{zodiac}/today/'
    responce_result = await get_responce(link=url)
    soup: BeautifulSoup = BeautifulSoup(markup=responce_result, features='lxml')
    text = soup.find(name='div', class_='article__text')
    return text.text


