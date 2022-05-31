Описание модуля
===
Этот модуль скачивает книги из открытой библиотеки [tululu.org](https://tululu.org). Модуль сделан в учебных целях.

Установка и подготовка к работе
---
Необходимо установить библиотеки из файла `requirements.txt`. Это делается командой в консоли:
```
pip install -r requirements.txt
```

Описание работы модуля и функций
---
Программа запускается командой в консоли:
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