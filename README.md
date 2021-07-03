# Сайт «Продуктовый помощник»
![foodgram project workflow](https://github.com/drowsycoder/foodgram-project/actions/workflows/foodgram_workflow.yml/badge.svg)

«Продуктовый помощник» — дипломный проект курса «Python-разработчик» от Яндекс.Практикум.

Это онлайн-сервис, где пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

### Предварительные требования

Необходимо установить Docker с официального [сайта](https://www.docker.com/products/docker-desktop).

### Пример работы сервиса

[Находится здесь](http://178.154.230.234/).

### Информация по работе с проектом (в режиме работы с контейнерами)

0. Клонирование проекта:
```
git clone https://github.com/drowsycoder/foodgram-project.git
```
1. Загрузка контейнеров с [DockerHub](https://hub.docker.com/repository/docker/drowzycoder/foodgram_project). Запуск (из корневой директории проекта при активном Docker):
```
docker pull drowzycoder/foodgram_project
docker-compose up -d --build
```
2. Вход в командную оболочку внутри контейнера:
```
docker exec -it <container_id> bash
```
3. Создание миграций (в командной оболочке):
```
python manage.py migrate
```
4. Создание суперпользователя (в командной оболочке):
```
python manage.py createsuperuser
```
5. Сбор статики:
```
python manage.py collectstatic --no-input
```
6. Запуск сервера по адресу http://127.0.0.1/:
```
python manage.py runserver
```
7. Загрузка тестовых данных:
```
docker-compose exec web python manage.py loaddata fixtures.json
```