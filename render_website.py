import json
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server, shell
from more_itertools import chunked


def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('lib_template.html')

    with open('book_info.json', 'r', encoding='utf-8') as books_info:
        books_details = json.load(books_info)

    books_pages = list(chunked(books_details, 20))

    pages_dir = 'pages'

    os.makedirs(pages_dir, exist_ok=True)

    for page_num, books in enumerate(books_pages,1):

        books_rows = list(chunked(books, 2))

        rendered_page = template.render(
            book_card_details = books_rows
        )

        page_name = f'index{page_num}.html'
        page_path = os.path.join(pages_dir, page_name).replace('\\','/')

        with open(page_path, 'w', encoding="utf8") as file:
            file.write(rendered_page)

on_reload()

server = Server()
server.watch('index.html', on_reload)
server.serve(root='.')