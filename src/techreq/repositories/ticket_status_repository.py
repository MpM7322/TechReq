from techreq.database.techreq_db import get_connection
from techreq.models.ticket_status import TicketStatus

# Вспомогательная функция преобразования данных
def _map(row) -> TicketStatus:
    return TicketStatus(*row)

# Функция для получения всех записей
def get_all() -> list[TicketStatus]:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT ticket_status_id, name
        FROM ticket_status
        ORDER BY ticket_status_id
    """)

    rows = cur.fetchall() # Преобразование всех записей в кортежи
    conn.close()

    return [_map(lines) for lines in rows]

# Функция для вывода всей информации о статусе заявки по ID
def get_by_id(ticket_status_id: int) -> TicketStatus | None:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT ticket_status_id, name
        FROM ticket_status
        WHERE ticket_status_id = ?
    """, (ticket_status_id,))

    row = cur.fetchone() # Возвращает одну запись из БД
    conn.close()

    return _map(row) if row else None