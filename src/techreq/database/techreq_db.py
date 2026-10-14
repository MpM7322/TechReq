import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent # Папка работы
SCHEMA_PATH = BASE_DIR / "schema.sql" # Файл sql схемы
DB_PATH = BASE_DIR / "techreq.db" # Файл, где будет ДБ

# Инициализация ДБ
def init_db():
    with open(SCHEMA_PATH, encoding="utf-8") as f: script = f.read() # Читаем наш SQL код в script
    conn = sqlite3.connect(DB_PATH) # Подключение к БД(Если её нет, то она создатся)
    try:
        conn.executescript(script) # Выполняет sql script, создавая описанные таблицы
        conn.commit() # Сохранение таблиц из sql скрипта
    finally: conn.close() # Закрытие БД, 

    print("\n\nБаза данных создана.")

# Будут выведены все таблички только в том случае, если запускается techreq_db.py(Этот файл)
if __name__ == "__main__":
    init_db()
    for name in ("user_roles", "ticket_categories", "ticket_status", "users", 
                  "tickets", "ticket_resolutions", "executor_categories"): 
            conn = sqlite3.connect(DB_PATH)
            try: tables = conn.execute(f"SELECT * FROM {name}").fetchall() # SQL запрос на получение всех столбцов из нужной таблицы
            # fetchall превращает все строки таблиц из БД в список кортежей 
            finally: conn.close()
            print(f"\n\n===== {name} =====")
            for table in tables: print(table)