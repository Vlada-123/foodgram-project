# Сайт «Продуктовый помощник»
![foodgram project workflow](https://github.com/drowsycoder/foodgram-project/actions/workflows/foodgram_workflow.yml/badge.svg)

«Продуктовый помощник» — дипломный проект курса «Python-разработчик» от Яндекс.Практикум.

Это онлайн-сервис, где пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

### Предварительные требования

Необходимо установить Docker с официального [сайта](https://www.docker.com/products/docker-desktop).


### Информация по работе с проектом (в режиме разработки)

0. Клонирование проекта:
```
git clone https://github.com/drowsycoder/foodgram-project.git
```   
1. Установка зависимостей (работа производится в виртуальном окружении):
```
pip install -r requirements.txt
```
2. Создание миграций:
```
python manage.py makemigrations
python manage.py migrate
```
3. Создание суперпользователя в командной оболочке контейнера:
```
python manage.py createsuperuser
```
4. Сбор статики:
```
python manage.py collectstatic --no-input
```
5. Запуск сервера по адресу http://127.0.0.1/ (должен быть подготовлен PostreSQL, иначе заменить настройки проекта на настройки Django по умолчанию для работы с sqlite3):
```
python manage.py runserver
```