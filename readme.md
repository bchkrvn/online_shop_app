# ONLINE-SHOP APP

## Описание:
В данном проекте реализован онлайн-магазин продуктов питания.

## Используемые технологии:
* <img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original.svg" width="25"> Python 3.9
* <img src="https://github.com/devicons/devicon/blob/master/icons/django/django-plain.svg" width="25"> Django 4.1.9
* <img src="https://github.com/devicons/devicon/blob/master/icons/postgresql/postgresql-original.svg" width="25">  Postgres
* <img src="https://github.com/devicons/devicon/blob/master/icons/redis/redis-original.svg" width="25">  Redis
* <img src="https://github.com/devicons/devicon/blob/master/icons/docker/docker-original.svg" width="25">  Docker
* Rabbitmq
* Celery

## Возможности проекта:
Видео на Youtube:
[![Watch the video](https://img.youtube.com/vi/HWYuS3iw2mw/maxresdefault.jpg)](https://youtu.be/HWYuS3iw2mw)

* Регистрация, аутентификация, смена пароля через почту.
* Список продуктов, детальная информация о продукте
* Корзина, оформление заказа, уведомление о заказе на email
* Рекомендации к продуктам в корзине
* Личный кабинет пользователя с информацией о заказах
* Подробная информация о заказе
* Сайт доступен на русском и английском языках

## Запуск проекта:
1) Сделать копию данного репозитория:   
`git clone https://github.com/bchkrvn/online_shop_app.git`
2) Перейти в папку **docker** и создать переменные окружения в файлах app.env и db.env.  

В **docker.env** нужно задать следующие параметры:
```
DB_NAME
DB_USER
DB_PASSWORD
DB_HOST
DB_PORT
EMAIL_HOST
EMAIL_HOST_USER
EMAIL_HOST_PASSWORD
EMAIL_PORT
DEBUG
CELERY_BROKER_URL
DJANGO_SETTINGS_MODULE
SECRET_KEY
REDIS_HOST
REDIS_PORT
REDIS_DB
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_DB
```

3) Выполнить команду:
`docker-compose up -d`