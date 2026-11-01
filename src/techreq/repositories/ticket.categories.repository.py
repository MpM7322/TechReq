from src.techreq.database.techreq_db import get_connection
from src.techreq.models.ticket_category import TicketCategory

# Вспомогательная функция преобразования данных
def _map(row) -> TicketCategory:
    return TicketCategory(*row)

# Функция для получения всех записей
def get_all() -> list[TicketCategory]:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT category_id, name
        FROM ticket_categories
        ORDER BY category_id
    """)

    rows = cur.fetchall() # Преобразование всех записей в кортежи
    conn.close()

    return [_map(lines) for lines in rows]

# Функция для вывода всей информации о роли по ID
def get_by_id(category_id: int) -> TicketCategory | None:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT category_id, name
        FROM ticket_categories
        WHERE category_id = ?
    """, (category_id))

    row = cur.fetchone() # Возвращает одну запись из БД
    conn.close()

    return _map(row) if row else None