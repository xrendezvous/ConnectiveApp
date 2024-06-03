# Connective

## Про програму
Connective - це веб-додаток, створений на фреймворку Django, який надає користувачам інструменти для керування контактами та нотатками, завантаження файлів у хмарне сховище та отримання новин. Додаток включає механізми автентифікації для забезпечення конфіденційності та безпеки даних користувачів.

## Вимоги
Для запуску цього додатку потрібні ключі API. Отримайте необхідні ключі за вказаними нижче адресами:
* Створіть обліковий запис на **[openweathermap.org](https://openweathermap.org)**, потім перейдіть на **[openweathermap.org/api_keys](https://home.openweathermap.org/api_keys)** і створіть ключ API для доступу.
* Створіть обліковий запис на **[abstractapi.com](https://www.abstractapi.com)**. Потім перейдіть на **[abstractapi.com/api](https://app.abstractapi.com/api/ip-geolocation/tester)** і створіть ключ API для доступу.
* Створіть обліковий запис на **[cloudinary.com](https://cloudinary.com)**. Потім перейдіть на сторінку налаштувань і згенеруйте ключі доступу.

Також рекомендовано встановити додатки Docker Desktop для керування контейнерами та DBeaver для перегляду бази даних.

Клонуйте репозиторій
```bash
  git clone https://github.com/xrendezvous/ConnectiveApp
```
Переконайтеся, що у вас встановлено poetry, якщо ні - підключіть командою 
```bash
  pip install poetry
```
Після цього створіть віртуальне середовище
```bash
  poetry shell
```
Перевірте, чи робите ви це в потрібній вам директорії

Встановлення залежностей
```bash
  poetry install
```

Тепер відкрийте файл .env.example і заповніть поля для потрібних вам змінних:
* SECRET_KEY=ваш django-secret-key
* API_WEATHER_KEY=ваш weather-key
* ABSTRACT_API_KEY=ваш abstract-key
* CLOUDINARY_NAME=ім'я вашої хмари
* CLOUDINARY_API_KEY= ваш ключ до хмари
* CLOUDINARY_API_SECRET=ваш cloudinary-api-secret
* DB_ENGINE=django.db.backends.postgresql_psycopg2
* DB_USER=ваше ім'я користувача
* DB_PASSWORD=ваш пароль
* DB_NAME=назва вашої бази даних
* DB_HOST=ваш локальний хост
* DB_PORT=ваш порт

Збережіть цей файл як .env

Запустити файл Docker Compose
```bash
  docker compose up
```

Виконайте міграцію для вашої бази даних
```bash 
  python manage.py makemigrations
```

Мігруйте вашу базу даних
```bash 
  python manage.py migrate
```

Запустіть сервер
```bash
  python manage.py runserver
```

За замовчуванням, додаток буде запущено на [http://127.0.0.1:8000/](...)
