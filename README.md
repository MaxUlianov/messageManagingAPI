## Сервис отправки сообщений (уведомлений)

Сервис реализован с помощью фреймворка Django / DRF
Для отправки сообщений по расписанию используется Celery с Redis в качестве брокера

### Установка проекта с зависимостями
#### Python libraries, Django
pip install -r requirements.txt

#### Установка, запуск Redis

sudo apt install redis
redis-server

#### Запуск Celery worker

celery -A messageManager worker --loglevel=INFO

### Запуск проекта
python -m manage.py runserver


### API
