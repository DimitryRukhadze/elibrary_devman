import os

import requests

url = "https://tululu.org/txt.php"

def download_books(books_url):

    url = books_url

    books_dir = 'books'
    os.makedirs(books_dir, exist_ok=True)

    for book_id in range(1, 10):
        params = {
            'id': book_id
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        with open(f'{books_dir}/{book_id}.txt', 'w', encoding='utf-8') as dvmn_pic:
            dvmn_pic.write(response.text)

download_books(url)