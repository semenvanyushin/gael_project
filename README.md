# Игровой портал Gael
![Python](https://img.shields.io/badge/Python-3.10.9-green)
![Django](https://img.shields.io/badge/Django-4.1.6-blue)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.0-%238b00ff)

## Описание проекта:
Gael - вебсайт, который дает возможность совместно приобретать игры для платформы Playstation. Купленные игры можно продавать другим пользователям. Пользователи могут оставлять отзывы друг на друга с присвоением рейтинга.

### Запуск в режиме разработчика:

Создание и активация виртуального окружения:
```bash
python3 -m venv venv # MacOS и Linux
python -m venv venv # Windows
```
```bash
source venv/bin/activate # MacOS и Linux
source venv\Scripts\activate # Windows
```
Установка зависимостей из файла requirements.txt:
```bash
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```
Выполнение миграций(выполняется из директории с файлом manage.py):
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```
Запуск сервера(выполняется из директории с файлом manage.py):
```bash
python3 manage.py runserver
```

Автор: [Семен Ванюшин](https://github.com/semenvanyushin)