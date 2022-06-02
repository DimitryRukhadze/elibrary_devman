import os
import argparse
import logging

from urllib.parse import urljoin, urlsplit, unquote


import requests

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from retry import retry


def check_for_redirect(response_to_check):
    if response_to_check.history:
        raise requests.HTTPError


def download_txt(filename, id_number, folder='books/'):

    txt_url = "https://tululu.org/txt.php"

    params = {
        'id': id_number
    }
    response = requests.get(txt_url, params=params)
    response.raise_for_status()

    check_for_redirect(response)

    os.makedirs(folder, exist_ok=True)

    filename = f'{id_number}. {filename}'
    valid_filename = sanitize_filename(filename)
    filepath = os.path.join(folder, valid_filename)

    with open(f'{filepath}.txt', 'w', encoding='utf-8') as book:
        book.write(response.text)

    return filepath


def download_image(img_url, img_folder):

    response = requests.get(img_url)
    response.raise_for_status()

    file_local_path = urlsplit(unquote(img_url)).path
    filename = os.path.basename(file_local_path)

    filepath = os.path.join(img_folder, filename)

    with open(filepath, 'wb') as book_img:
        book_img.write(response.content)


def parse_book_page(book_page_html, book_page_url):

    book_soup = BeautifulSoup(book_page_html, 'lxml')
    book_title_tag = book_soup.find('body').find('table', class_='tabs').find('h1')
    book_img_rel_url = book_soup.find('div', class_='bookimage').find('img')['src']
    book_comments_tags = book_soup.find_all('div', class_='texts')
    book_genre_tags = book_soup.find('span', class_='d_book').find_all('a')

    book_comments = [
        comment.find('span', class_='black').text
        for comment in book_comments_tags
    ]

    book_genres = [
        genre.text
        for genre in book_genre_tags
    ]

    book_img_full_url = urljoin(book_page_url, book_img_rel_url)

    book_props = book_title_tag.text.split('::')
    book_name, book_author = book_props

    book_description = {
        'title': book_name.strip(),
        'author': book_author.strip(),
        'img url': book_img_full_url,
        'comments': book_comments,
        'genres': book_genres
    }

    return book_description


@retry(requests.ConnectionError, delay=1)
def main():
    parser = argparse.ArgumentParser(description='Программа скачивает книги')
    parser.add_argument('start_id', help='Starting book id', type=int)
    parser.add_argument('end_id', help='Final book id', type=int)
    args = parser.parse_args()

    logging.basicConfig(format=f'%(levelname)s %(message)s')

    books_dir = 'books'
    img_dir = 'images'
    os.makedirs(books_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)

    for book_id in range(args.start_id, args.end_id + 1):
        try:
            book_page_url = f"https://tululu.org/b{book_id}/"

            response = requests.get(book_page_url)
            response.raise_for_status()

            check_for_redirect(response)

            book_info = parse_book_page(response.text, book_page_url)

            download_image(book_info['img url'], img_dir)
            download_txt(book_info['title'], book_id, folder=books_dir)

        except requests.HTTPError:
            logging.warning('There is no book with such id. Trying next id...')


if __name__ == '__main__':
    main()
