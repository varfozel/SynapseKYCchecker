import aiohttp
import asyncio
from urllib.parse import urlparse, parse_qs


def read_file_lines(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]


def get_session(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    session_id = query_params.get('session_id', [None])[0]
    return session_id


async def check_status(session, url, headers):
    session_id = get_session(url)
    async with session.get(f'https://api.synaps.io/individual/session/{session_id}', headers=headers) as response:
        data = await response.json()
        return data['session']['status']


async def check():
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'no-cache',
        'origin': 'https://verify.synaps.io',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://verify.synaps.io/',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    }

    links = read_file_lines('Links.txt')

    async with aiohttp.ClientSession() as session:
        tasks = [check_status(session, link, headers) for link in links]
        results = await asyncio.gather(*tasks)

        with open('kyc_result.txt', 'a') as file:
            for status in results:
                file.write(f"{status}\n")


asyncio.run(check())
