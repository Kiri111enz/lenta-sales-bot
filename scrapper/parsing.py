from bs4 import BeautifulSoup
import os
import shutil
from aiohttp import ClientSession
import asyncio
import json


async def collect_data(loop, city: str = 'nsk', store: int = 80):
    main_folder = 'current_sales'
    # TODO: delete outadeted files
    # shutil.rmtree(main_folder)
    # os.makedirs(main_folder)
    print('Outdated files have been deleted')

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;'
                  'q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/102.0.5005.134 Mobile Safari/537.36'
    }
    cookies = {
        'CityCookie': city,
        'Store': '{:04}'.format(store)
    }
    main_url = 'https://lenta.com'
    async with ClientSession(loop=loop) as session:
        print('Session have been opened')
        response = await session.get(url=main_url + '/promo', headers=headers, cookies=cookies)
        soup = BeautifulSoup(await response.text(), 'lxml')
        categories = soup.find_all('li', class_='catalog-tree__category')

        for category in categories:
            category_name = category.find('a', class_='link link--black catalog-tree__link catalog-link '
                                                      'catalog-link--category'
                                          ).text.strip().replace('/', ' или ').replace('"', '')

            category_folder = f'{main_folder}/{category_name}'
            os.makedirs(category_folder)

            subcategories = category.find_all('li', class_='catalog-tree__subcategory')
            for subcategory in subcategories:
                # print(subcategory)
                subcategory_name = subcategory.find('a', class_='link link--gray catalog-tree__link catalog-link'
                                                    ).text.strip().replace('/', ' или ').replace('"', '')
                adding_url = subcategory.find('a', class_='link link--gray catalog-tree__link catalog-link')['href']

                response = await session.get(url=main_url + adding_url, headers=headers, cookies=cookies)
                soup = BeautifulSoup(await response.text(), 'lxml')

                data = []
                cards = soup.find_all('div', class_='sku-card-small-container js-sku-card-small')
                for card in cards:
                    info = {
                        'title': json.loads(card['data-model'])['title'],
                        'sale_percent': json.loads(card['data-model'])['promoPercent'],
                        'card_price': float(json.loads(card['data-model'])['cardPrice']['value']),
                        'regular_price': float(json.loads(card['data-model'])['regularPrice']['value']),
                        'sale_start': json.loads(card['data-model'])['promoStart'].replace('T', ' '),
                        'sale_end': json.loads(card['data-model'])['promoEnd'].replace('T', ' '),
                        'url': main_url + card.find('a')['href']
                    }
                    data.append(info)
                '''
                try:
                    page_count = int(soup.find('li', class_='next').find('a')['rel'][2])
                except AttributeError:
                    continue
                '''

                # print(len(data))

                try:
                    with open(f'{category_folder}/{subcategory_name}.json', 'w', encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=4)
                    print(f'{subcategory_name}.json added')
                except FileExistsError:
                    print(f"Outdate file on path {category_folder}/{subcategory_name}.json haven't been deleted")

                # exit(0)
    print('Session have been closed')


async def collect_subcategory_data(url, session):
    response = await session.get(url=url, )


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(collect_data(loop=loop))
