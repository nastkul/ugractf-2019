# Emoji Translator I: Write-up

1. Установить Python 3

2. Поставить зависимости
   
   ```
   py -3 -m pip install flask peewee
   ```

3. Исправить ошибки
   
   * `temlpates` → `templates`
   * `class Emoji:` → `class Emoji(Model):`
   * `app = Flask(__name__)`
   * Установить PostgreSQL или поменять БД на SQLite:  
     `db = SqliteDatabase('translator.sqlite')`
