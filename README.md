# Проект api на базе FastAPI

# Установка. 
## Следуйте следующим команда для установки и развертывание проекта у себя локально 
### Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/Sava151/QRkot_spreadsheets.git
```
### Cоздать и активировать виртуальное окружение:
#### Рекомендуется использовать python 3.9
```
cd cat-charity-1/
```
```
py -3.9 -m venv venv
```
```
source venv/Scripts/activate
```
#### Уточнение имеющихся версий python 
```
py -0
```
#### Уточнение версии по умолчанию
```
python --version 
```
### Установить зависимости из файла requirements.txt
```
pip install -r requirements.txt
```
### Запустить проект
```
 alembic upgrade head
```
```
 uvicorn app.main:app
```
# Стек технологий 
## Версия Python 3.9
## СУБД
* SQLite 3 с асинхронным драйвером aiosqlite
## Сторонние библиотеки
* fastapi
* pydantic
* alembic
* SQLAlchemy
* aiosqlite

## Документация
[Swagger](http://127.0.0.1:8000/docs#/)
[ReDoc](http://127.0.0.1:8000/redoc)


### Об авторе
[Sava151](https://github.com/Sava151)
Савелий Олегович
savely.olegovich@yandex.ru