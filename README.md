# CreateLearn
Платформа для людей, желающих учиться, и тех, кто готов делиться знаниями

## Запуск

1. Создать файл `.env`, прописать значения указанные в `.env.example`
   
2. Создать виртуальное окружение и активировать
   
```sh
python -m venv .venv
source .venv/bin/activate
```

3. Установка зависимостей
```sh
pip install -r requirements.txt
```

4. Проведение миграций
```sh
python manage.py migrate
```

5. Запустить сервер
```sh
python manage.py runserver
```

6. Перейти на сайт по http://127.0.0.1:8000/

#### Проектный практикум - весна 2025
