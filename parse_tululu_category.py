import os
import logging
import json

from urllib.parse import urljoin, urlsplit


import requests
import main

from bs4 import BeautifulSoup
from dotenv import load_dotenv


def parse_book_urls(page_html, base_book_url):
    book_soup = BeautifulSoup(page_html, 'lxml')
    book_tabs = book_soup.select('.d_book .bookimage a')
    book_urls = [
        urljoin(base_book_url, book['href'])
        for book in book_tabs
    ]

    return book_urls


def puginate_book_urls():

    all_book_urls = []

    for page_num in range(1,5):
        sci_fi_url = f'https://tululu.org/l55/{page_num}'

        result = requests.get(sci_fi_url)
        result.raise_for_status()

        all_book_urls.extend(parse_book_urls(result.text, sci_fi_url))

    return all_book_urls


if __name__ == '__main__':
    load_dotenv()

    logging.basicConfig(format=f'%(levelname)s %(message)s')

    books_dir = os.environ.get('BOOKS_DIR')
    img_dir = os.environ.get('IMAGES_DIR')

    os.makedirs(books_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)

    book_urls = puginate_book_urls()
    books_info = []

    for url in book_urls:
        try:
            response = requests.get(url)
            response.raise_for_status()

            main.check_for_redirect(response)

            book_info = main.parse_book_page(response.text, url)
            books_info.append(book_info)
            book_id = urlsplit(url).path.strip('/')[1:]

            main.download_image(book_info['img url'], img_dir)
            main.download_txt(book_info['title'], book_id, folder=books_dir)

        except requests.HTTPError:
            logging.warning('There is no book with such id. Trying next id...')

    with open('book_info.json', 'w', encoding='utf-8') as json_file:
        json.dump(books_info, json_file, ensure_ascii=False)