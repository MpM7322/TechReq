from src.techreq.database.techreq_db import get_connection
from src.techreq.models.user_role import UserRole

# Вспомогательная функция преобразования данных
def _map(row) -> UserRole:
    return UserRole(*row)

# Функция для получения всех записей
def get_all() -> list[UserRole]:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT user_role_id, name
        FROM user_roles
        ORDER BY user_role_id
    """)

    rows = cur.fetchall() # Преобразование всех записей в кортежи
    conn.close()

    return [_map(lines) for lines in rows]

# Функция для вывода всей информации о роли по ID
def get_by_id(user_role_id: int) -> UserRole | None:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT user_role_id, name
        FROM user_roles
        WHERE user_role_id = ?
    """, (user_role_id))

    row = cur.fetchone() # Возвращает одну запись из БД
    conn.close()

    return _map(row) if row else None