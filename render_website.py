import json

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

    chunked_book_details = list(chunked(books_details, 2))

    rendered_page = template.render(
        book_card_details = chunked_book_details
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

on_reload()

server = Server()
server.watch('index.html', on_reload)
server.serve(root='.')