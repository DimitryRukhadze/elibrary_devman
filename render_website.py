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

    html_dir = 'pages'
    os.makedirs(html_dir, exist_ok=True)

    pages_of_books_details = list(chunked(books_details, 20))

    all_pages_links = [
        f'index{page_num + 1}.html'
        for page_num in range(len(pages_of_books_details))
    ]

    for page_num, details in enumerate(pages_of_books_details):

        books_rows = list(chunked(details, 2))

        page_name = all_pages_links[page_num]
        page_path = os.path.join(html_dir, page_name).replace('\\','/')

        rendered_page = template.render(
            book_card_details = books_rows,
            all_pages = all_pages_links,
            curr_name = page_path
        )

        with open(page_path, 'w', encoding="utf8") as file:
            file.write(rendered_page)


on_reload()

server = Server()
server.watch('pages/*.html', on_reload)
server.serve(root='pages/', default_filename='index1.html')