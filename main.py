import os

import requests

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename

url = "https://tululu.org/txt.php"

def check_for_redirect(response_to_check):
    if response_to_check.history:
        raise requests.HTTPError


def download_txt(txt_url, filename, id_number, folder='books/'):

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


def get_book_title(book_id):

    book_info_url = f"https://tululu.org/b{book_id}/"

    response = requests.get(book_info_url)
    response.raise_for_status()

    book_soup = BeautifulSoup(response.text, 'lxml')
    book_title_tag = book_soup.find('body').find('table', class_='tabs').find('h1')
    book_props = book_title_tag.text.split('::')
    book_name = book_props[0].strip()

    return book_name


if __name__ == '__main__':

    url = "https://tululu.org/txt.php"

    books_dir = 'books'
    os.makedirs(books_dir, exist_ok=True)

    for book_id in range(1,11):
        book_title = get_book_title(book_id)
        try:
            download_txt(url, book_title, book_id, folder=books_dir)
        except requests.HTTPError:
            continue
