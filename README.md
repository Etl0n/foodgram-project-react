# Продуктовый помощник
### Технологии:
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/) [![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/) [![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/) [![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/) [![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/) [![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/) [![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
## Описание проекта:

#### Foodgram - это онлайн-сервис, который представляет собой «Продуктовый помощник». На этом сервисе пользователи могут делиться своими рецептами, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», подписываться на понравившихся им пользователей. Кроме того, они могут скачивать сводный список продуктов, необходимых для приготовления выбранных блюд перед походом в магазин.
## Запуск проекта на сервере:

#### Склонировать репозиторий
> git@github.com:Etl0n/foodgram-project-react.git

## Подготовка сервера:

#### Обновить индекс пакетов APT
>sudo apt update 

#### Обновите установленные в системе пакеты и установите обновления безопасности
>sudo apt upgrade -y

#### Установить менеджер пакетов pip, утилиту для создания виртуального окружения venv, систему контроля версий git, чтобы клонировать ваш проект.
>sudo apt install python3-pip python3-venv git -y

#### Установите на свой сервер Docker
>sudo apt install docker.io

#### Установите docker-compose
>sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

>sudo chmod +x /usr/local/bin/docker-compose

#### Добавьте в Secrets GitHub переменные окружения:

* DOCKER_USERNAME (имя на DockerHub)
* DOCKER_PASSWORD (пароль на DockerHub)
* HOST (ip адрес вашего сервера)
* USER (имя пользователя на сервере)
* SSH_KEY (SSH ключ от сервера)
* TELEGRAM_TO (ваш id в телеграме, чтобы отправить уведомления о успешном деплое проекта на сервер)
* TELEGRAM_TOKEN (TOKEN любого вашего бота в Telegram)

#### Со своего компьютера сделать коммит, чтобы деплой на сервер произошел автоматически

#### Собрать контейнеры на удалённом сервере
>sudo docker compose -f docker-compose.production.yml up --build -d

## Проект доступен по [адресу](https://foodgramworld.ddns.net/)

## Автор
https://github.com/Etl0n (Ученик Яндекс Практикум)
