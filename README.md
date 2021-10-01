# Инструкция по запуску

## 1) Elasticsearch
Для начала запускаем сервер Elasticsearch у себя на машине.

## 2) models.py
Затем создаем модели в базе данных. Для этого запускаем *models.py* со своими
данными для подключения к БД.

![Screenshot](images/models_data.png)

## 3) db_worker.py
Здесь тоже указываем свой путь для подключения к базе данных и запускаем скрипт. После этого
данные из csv-файла загрузятся в БД.

![Screenshot](images/db_worker_data.png)

## 4) elasticsearch_worker.py
Запускаем этот скрипт, чтобы все данные так же загрузились и в индекс. Придется немного 
подождать.

## 5) app.py
Запускаем *app.py*, и все готово! Теперь можно начинать работать с сервером.


# Примеры запросов и ответы на них:
### GET - запрос

![Screenshot](images/get1.png)
![Screenshot](images/get2.png)

### DELETE - запрос

![Screenshot](images/delete1.png)
![Screenshot](images/delete2.png)
