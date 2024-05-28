# Продуктовый помощник
## Технологии:
---
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/) [![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/) [![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/) [![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/) [![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/) [![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/) [![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
## Описание проекта:
---
#### Foodgram - это онлайн-сервис, который представляет собой «Продуктовый помощник». На этом сервисе пользователи могут делиться своими рецептами, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», подписываться на понравившихся им пользователей. Кроме того, они могут скачивать сводный список продуктов, необходимых для приготовления выбранных блюд перед походом в магазин.
## Как запустить приложение:
---
### 1. Запуск приложения локально(лучше пользоваться этим вариантом так как он более простой):
#### Склонировать репозиторий на свой компьютер
> git@github.com:Etl0n/foodgram-project-react.git
#### Создать файл .env с данными для подключения к БД
* POSTGRES_DB = 
* POSTGRES_USER =
* POSTGRES_PASSWORD =
* DB_NAME = 
* DB_HOST = db
* DB_PORT = 5432
#### Собрать докер-контейнеры в единую сеть для этого выполните эту команду из директории где лежит файл docker-compose.production.yml
> docker compose -f docker-compose.production.yml up -d
#### По очередно выполните эти команды в этой же директории
* >docker compose -f docker-compose.production.yml exec backend python manage.py migrate
* >docker compose -f docker-compose.production.yml exec backend python manage.py import_csv ./data/ingredients.csv
* >docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
* >docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /backend_static/static/
#### После проделанной работы приложение будет доступно по ссылке (https://localhost:7000)
### 2. Запуск прилоения на сервере
#### (для этого на сервере уже должен быть установлен docker и nginx, прописана конфигурация файла nginx чтобы он перенаправлял все запросы приходящие на сервер(proxy_pass http://127.0.0.1:7000)):
#### Форкнуть репозиторий себе в GitHub:
> Для этого найдите кнопку Fork немного выше и правее центра экрана
#### Склонировать форкнутый репозиторий себе на компьютер:
> git clone (SSH ссылка на форкнутый репозиторий)
#### Добавьте в Secrets GitHub переменные окружения:
>Для начала перейдите в Settings репозитория, затем Secrets and variables, добавте эти значения
* DOCKER_USERNAME (имя на свой DockerHub)
* DOCKER_PASSWORD (пароль на свой DockerHub)
* HOST (ip адрес вашего сервера)
* USER (имя пользователя на сервере)
* SSH_KEY (SSH ключ от сервера)
* TELEGRAM_TO (ваш id в телеграме, чтобы отправить уведомления о успешном деплое проекта на сервер)
* TELEGRAM_TOKEN (TOKEN любого вашего бота в Telegram)
#### Со своего компьютера сделать push из репозитория, чтобы деплой на сервер произошел автоматически
> git push
## Автор
---
https://github.com/Etl0n (Ученик Яндекс Практикум)
