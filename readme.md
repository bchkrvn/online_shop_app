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
* Регистрация, аутентификация, смена пароля через почту.
* Список продуктов, детальная информация о продукте
* Корзина, оформление заказа, уведомление о заказе на email
* Рекомендации к продуктам в корзине
* Личный кабинет пользователя с информацией о заказах
* Подробная информация о заказе

## Запуск проекта:
1) Сделать копию данного репозитория:   
`git clone https://github.com/bchkrvn/online_shop_app.git`
2) Перейти в папку **docker** и создать переменные окружения в файлах app.env, db.env, rabbitmq.env.  
В app.env нужно задать следующие параметры:
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
RABBITMQ_DEFAULT_USER
RABBITMQ_DEFAULT_PASS
SECRET_KEY
REDIS_HOST
REDIS_PORT
REDIS_DB
```
В db.env:
```
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_DB
```
в rabbitmq.env:
```
RABBITMQ_DEFAULT_USER
RABBITMQ_DEFAULT_PASS
```
3) выполнить команду:
`docker-compose up -d`