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
Описание API со Swagger UI (дополнительное задание 5) доступно по адресу /docs

Описание в формате OpenAPI находится в файле openapi-schema.yml
(включая требуемые параметры запроса)

Краткое описание API:

Рассылки:
/manager/api/mailings

GET: список рассылок
POST: создать рассылку

Управление рассылкой по id
/manager/api/mailing/{mailing_id}

GET: данные рассылки
PUT: обновление рассылки
DELETE: удаление рассылки

Клиенты:
/manager/api/clients

GET: список клиентов
POST: добавление нового клиента

Управление данными клиента по id:
/manager/api/client/{client_id}

GET: данные клиента
PUT: обновление данных клиента
DELETE: удаление клиента из базы


Сообщения
/manager/api/messages

GET: список сообщений


(панель администрирования – доп. пункт 6 – по умолчанию встроена в Django по адресу /admin)
