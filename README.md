## requirements
для работы приложения необходимы следующие зависимости:
  - python3
  - django (при отладке использовалась версия 2.2)
  - база данных (есть несколько вариантов настроек в tinkoffJournal/settings.py)

## Инициализация базы
Выбор бызы данных в tinkoffJournal/settings.py. По дифолту указан облачный инстанс postgresql для использования которого не требуется дополнительная установка (но тогда тесты конфликтуют с продакшен данными)

Создание схемы базы:
```python3 manage.py migrate articles```

Заполнение начальными/пробными данными (при желании):
```python3 manage.py loaddata seed_data.json```

## Запуск сервиса
Для пробного запуска достаточно выполнить:
  ```python3 manage.py runserver```

И сервис запустится локально на 8000-м порту:
  ```http://127.0.0.1:8000/api/v1/articles/?names=longread/yet-another-article,news/some-article-shortname,news/other-shortname,longread/yet-another-article```

## Запуск тестов
При использовании полноценной базы, тесты можно запустить так:
  ```python3 manage.py test```

Но при использовании облачной (дефолтной) базы, следует использовать keepdb:
  ```python3 manage.py test --keepdb```
