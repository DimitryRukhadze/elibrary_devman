Описание модуля
===
Этот модуль скачивает книги из открытой библиотеки [tululu.org](https://tululu.org) и собирает сайт-библиотеку со скачанными 
книгами. Пример сайта (без обложек и возможности чтения книг) [на Github Pages](https://dimitryrukhadze.github.io/elibrary_devman/pages/index1.html).
Модуль сделан в учебных целях.

Установка и подготовка к работе
---
Необходимо установить библиотеки из файла `requirements.txt`. Это делается командой в консоли:
```
pip install -r requirements.txt
```
После этого вам необходимо создать в рабочей директории файл `.env` со следующим содержанием:
```dotenv
BOOKS_DIR='books'
IMAGES_DIR='images'
JSON_FILENAME='book_info.json'
```
Таким образом вы укажите названия директорий по умолчанию для скачивания книг (`BOOKS_DIR`), их обложек(`IMAGES_DIR`) и
имя JSON файла с дополнительной информацией по книгам. (`JSON_FILENAME`).

Описание работы main.py
---
Скрипт запускается командой в консоли:
```
python main.py 1 10
```
В этом примере скрипту передаётся два обязательных аргумента: '1' - id книги, с которого следует начать скачивание, '10' - 
id книги, которой следует завершить скачивание (включительно). Оба аргумента - числа, и они могут быть любыми, какие вы захотите.
Если вы их не передадите, консоль выведет следующее сообщение:
```
usage: main.py [-h] start_id end_id
main.py: error: the following arguments are required: start_id, end_id
```

После запуска программа создаст в директории из которой была запущена две папки `books` и `images`. В папку `books` будут скачаны
книги с id в интервале, который вы указали при запуске, если книги с такими id есть на сайте. В папку `images` будут скачаны
картинки обложек этих книг, если обложки есть.

Описание работы parse_tululu_category.py
---
Скрипт скачивает все книги из каталога "Научная фантастика". Он запускается командой в консоли:
```
python parse_tululu_category.py 12
```
В этом примере скрипту передаётся один аргумент `start_page` - номер страницы сайта с которой вы хотите скачать книги. Вот список аргументов,
которые можно передавать функции:

1. `start_page` - это обязательный аргумент, передаётся простым числом, описание и пример использования см. выше.

2. `--end_page` - необязательный аргумент. Если его передать, то скрипт будет скачивать книги со всех страниц сайта, начиная co 
`start_page` и заканчивая `--end_page`. Если стартовая страница будет больше, чем финальная, вы увидите в терминале сообщение
`WARNING The start_page arg is bigger than end_page`, после чего программа прекратит работу.

    Пример:
    ```
    python parse_tululu_category.py 12 --end_page 13
    ```

3. `--dest_folder` - необязательный аргумент. Если его передать, то скрипт создаст указанную директорию, и все файлы скачает в неё. 
   Пример:
    ```
    python parse_tululu_category.py 12 --dest_folder bookfiles
    ```

4. `--skip_imgs`- необязательный аргумент. Введите его, если не хотите скачивать обложки книг.
    Пример:
    ```
    python parse_tululu_category.py 12 --skip_imgs
    ```
5. `--skip_txt`- необязательный аргумент. Введите его, если не хотите скачивать книги.
    Пример:
    ```
    python parse_tululu_category.py 12 --skip_txt
    ```
6. `--json_path`- необязательный аргумент. Введите его, если хотите указать отдельный путь для .json файла с информацией о книгах.
   По умолчанию, файл будет создаваться в одной папке с директориями для книг и изображений.
    Пример:
    ```
    python parse_tululu_category.py 12 --json_path bookinfo
    ```

Описание работы render_website.py
---

Формирует по шаблону страницы сайта и запускает сервер livereload для их просмотра. После загрузки сервера сайт можно
увидеть в вашем браузере по адресу [http://127.0.0.1:5500/]( http://127.0.0.1:5500/). Сайт также работает оффлайн - просто откройте любую
из страниц в папке `pages`. Вы увидите в браузере сайт примерно такого вида:
![elibrary_screen](https://user-images.githubusercontent.com/77689849/177045108-04ca1ead-6d98-4ee4-91ea-02c6a1b8cd20.JPG)
