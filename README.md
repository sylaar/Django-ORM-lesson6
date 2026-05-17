# Блог им. Юрия Григорьевича

Блог о коммерческом успехе Юрия Григорьевича. Делюсь советами по бизнесу, жизни и о воспитании детей.

![Скриншот](screenshots/site.png)

## Запуск

Скачайте репозиторий
```sh
git clone https://github.com/sylaar/Django-ORM-lesson6.git
cd Django-ORM-lesson6
```

Установите зависимости
```sh
pip install -r requirements.txt
```

Скачайте [архив с данными](https://dvmn.org/media/modules_dist/sensive-blog-data.zip).
Положите базу данных и media из архива в папку с кодом рядом с `manage.py`

Примените миграции
```sh
python3 manage.py migrate
```

Запустите сервер

```
python3 manage.py runserver
```

## Переменные окружения

Часть настроек проекта берётся из переменных окружения. Чтобы их определить, создайте файл `.env` рядом с `manage.py` и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.

Доступны 3 переменные:
- `DEBUG` — дебаг-режим. Поставьте `True`, чтобы увидеть отладочную информацию в случае ошибки.
- `SECRET_KEY` — секретный ключ проекта
- `DATABASE_FILEPATH` — полный путь к файлу базы данных SQLite, например: `/home/user/schoolbase.sqlite3`
- `ALLOWED_HOSTS` — см [документацию Django](https://docs.djangoproject.com/en/5.2/ref/settings/#allowed-hosts)
