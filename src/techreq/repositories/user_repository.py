from techreq.database.techreq_db import get_connection
from techreq.models.user import User

# Вспомогательная функция преобразования данных
def _map(row) -> User:
    return User(*row)

# Функция для создания пользователя
def create(name: str, surname: str, patronymic: str, login: str, password: str, user_role: int) -> int:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO users(name, surname, patronymic, login, password, user_role)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, surname, patronymic, login, password, user_role,))

    user_id = cur.lastrowid

    conn.commit()
    conn.close()

    return user_id

# Функция для вывода всей информации о пользователе по ID
def get_by_id(user_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT u.user_id, u.name, u.surname, u.patronymic, u.login, u.password, u.user_role, r.name
        FROM users u
        JOIN user_roles r ON u.user_role = r.user_role_id
        WHERE u.user_id = ? 
    """, (user_id,))

    row = cur.fetchone() # Возвращает одну запись из БД
    conn.close()

    return _map(row) if row else None

# Функция для вывода всей информации о пользователе по login-у
def get_by_login(login: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT u.user_id, u.name, u.surname, u.patronymic, u.login, u.password, u.user_role, r.name
        FROM users u
        JOIN user_roles r ON u.user_role = r.user_role_id
        WHERE u.login = ? 
    """, (login,))

    row = cur.fetchone() # Возвращает одну запись из БД
    conn.close()

    return _map(row) if row else None

# Функция для получения всех записей
def get_all() -> list[User]:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT u.user_id, u.name, u.surname, u.patronymic, u.login, u.password, u.user_role, r.name
        FROM users u
        JOIN user_roles r ON u.user_role = r.user_role_id
        ORDER BY u.user_id
    """)

    rows = cur.fetchall() # Преобразование всех записей в кортежи
    conn.close()

    return [_map(lines) for lines in rows]

# Функция для удаления пользователя по id
def delete(user_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM users
        WHERE user_id = ?
    """, (user_id,))
    
    conn.commit()
    conn.close()
