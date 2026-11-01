from src.techreq.database.techreq_db import get_connection
from src.techreq.models.user import User

# Вспомогательная функция преобразования данных
def _map(row) -> User:
    return User(*row)

# Функция для создания пользователя
def create(name: str, surname: str, patronymic: str, login: str, password: str, user_role: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO users(name, surname, patronymic, login, password, user_role)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, surname, patronymic, login, password, user_role))

    conn.commit()
    conn.close()

# Функция для вывода всей информации о пользователе по ID
def get_by_id(user_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT user_id, name, surname, patronymic, login, password, user_role
        FROM users
        WHERE user_id = ? 
    """, (user_id))

    row = cur.fetchone() # Возвращает одну запись из БД
    conn.close()

    return _map(row) if row else None

# Функция для вывода всей информации о пользователе по login-у
def get_by_login(login: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT user_id, name, surname, patronymic, login, password, user_role
        FROM users
        WHERE login = ? 
    """, (login))

    row = cur.fetchone() # Возвращает одну запись из БД
    conn.close()

    return _map(row) if row else None

# Функция для получения всех записей
def get_all() -> list[User]:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT user_id, name, surname, patronymic, login, password, user_role
        FROM users
        ORDER BY surname, name, patronymic
    """)

    rows = cur.fetchall() # Преобразование всех записей в кортежи
    conn.close()

    return [_map(lines) for lines in rows]
