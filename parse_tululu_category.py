import os
import logging
import json
import argparse
from urllib.parse import urljoin, urlsplit

import requests
import main
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from retry import retry


def parse_book_urls(page_html, base_book_url):
    book_soup = BeautifulSoup(page_html, 'lxml')
    book_tabs = book_soup.select('.d_book .bookimage a')
    book_urls = [
        urljoin(base_book_url, book['href'])
        for book in book_tabs
    ]

    return book_urls


def puginate_book_urls(start_page, end_page=0):

    if not end_page:
        end_page = start_page + 1

    if end_page:
        end_page += 1

    all_book_urls = []

    for page_num in range(start_page, end_page):
        sci_fi_url = f'https://tululu.org/l55/{page_num}'

        result = requests.get(sci_fi_url)
        result.raise_for_status()

        all_book_urls.extend(parse_book_urls(result.text, sci_fi_url))

    return all_book_urls


@retry(requests.ConnectionError, delay=1)
def main_fn():
    load_dotenv()

    parser = argparse.ArgumentParser(description='Программа скачивает книги')
    parser.add_argument(
        'start_page',
        help='Starting book page',
        type=int
        )
    parser.add_argument(
        '--end_page',
        help='Final book page',
        type=int
        )
    parser.add_argument(
        '--dest_folder',
        help='Download folder',
        type=str
        )
    parser.add_argument(
        '--skip_imgs',
        help='Ввести, если не хотите скачивать обложки',
        action='store_true'
        )
    parser.add_argument(
        '--skip_txt',
        help='Ввести, если не хотите скачивать книги',
        action='store_true'
        )
    parser.add_argument(
        '--json_path',
        help='Указать путь для сохранения .json',
        type=str
        )
    args = parser.parse_args()

    logging.basicConfig(format=f'%(levelname)s %(message)s')

    books_dir = os.environ.get('BOOKS_DIR')
    img_dir = os.environ.get('IMAGES_DIR')
    json_file_save = 'book_info.json'

    if args.end_page and args.end_page < args.start_page:
        logging.warning('The start_page arg is bigger than end_page')
        raise
    if args.dest_folder:
        os.makedirs(args.dest_folder, exist_ok=True)
        books_dir = os.path.join(args.dest_folder, books_dir)
        img_dir = os.path.join(args.dest_folder, img_dir)
        if not args.json_path:
            json_file_save = os.path.join(args.dest_folder, json_file_save)
    if not args.skip_txt:
        os.makedirs(books_dir, exist_ok=True)
    if not args.skip_imgs:
        os.makedirs(img_dir, exist_ok=True)
    if args.json_path:
        os.makedirs(args.json_path, exist_ok=True)
        json_file_save = os.path.join(args.json_path, json_file_save)

    book_urls = puginate_book_urls(args.start_page, args.end_page)
    books_info = []

    for url in book_urls:
        try:
            response = requests.get(url)
            response.raise_for_status()

            main.check_for_redirect(response)

            book_info = main.parse_book_page(response.text, url)
            books_info.append(book_info)
            book_id = urlsplit(url).path.strip('/')[1:]

            if not args.skip_imgs:
                main.download_image(
                    book_info['img url'],
                    img_dir
                    )
            if not args.skip_txt:
                main.download_txt(
                    book_info['title'],
                    book_id,
                    folder=books_dir
                    )

        except requests.HTTPError:
            logging.warning('There is no book with such id. Trying next id...')

    with open(json_file_save, 'w', encoding='utf-8') as json_file:
        json.dump(books_info, json_file, ensure_ascii=False)


if __name__ == '__main__':
    main_fn()
