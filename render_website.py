import json
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server, shell
from more_itertools import chunked


BOOKS_ON_PAGE = 20
BOOKS_IN_ROW = 2


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

    pages_of_books_details = list(chunked(books_details, BOOKS_ON_PAGE))

    all_pages_links = [
        os.path.join(html_dir, f'index{page_num + 1}.html').replace('\\','/')
        for page_num in range(len(pages_of_books_details))
    ]

    for page_num, details in enumerate(pages_of_books_details):

        books_rows = list(chunked(details, BOOKS_IN_ROW))

        page_path = all_pages_links[page_num]
        prev_page = all_pages_links[page_num - 1]

        if page_num + 1 < len(all_pages_links):
            next_page = all_pages_links[page_num + 1]

        rendered_page = template.render(
            book_card_details = books_rows,
            all_pages = all_pages_links,
            curr_name = page_path,
            prev_page = prev_page,
            next_page = next_page
        )

        with open(page_path, 'w', encoding="utf8") as file:
            file.write(rendered_page)


if __name__ == '__main__':

    on_reload()

    server = Server()
    server.watch('pages/*.html', on_reload())
    server.serve(root='.', default_filename='pages/index1.html')