import json

from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('lib_template.html')

with open('book_info.json', 'r', encoding='utf-8') as books_info:
    books_details = json.load(books_info)

rendered_page = template.render(
    book_card_details = books_details
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)