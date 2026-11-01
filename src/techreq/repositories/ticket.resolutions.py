from src.techreq.database.techreq_db import get_connection
from src.techreq.models.ticket_resolution import TicketResolution

# Вспомогательная функция преобразования данных
def _map(row) -> TicketResolution:
    return TicketResolution(*row)

# Функция для написания ответа на заявку
def answer_ticket(ticket_id: int, solution_text: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO ticket_resolutions(ticket_id, solution_text)
        VALUES (?, ?)
    """, (solution_text, ticket_id))

    conn.commit()
    conn.close()

# Функция для получения всех записей
def get_all() -> list[TicketResolution]:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT resolution_id, ticket_id, solution_text
        FROM ticket_resolutions
    """)

    rows = cur.fetchall() # Преобразование всех записей в кортежи
    conn.close()

    return [_map(lines) for lines in rows]

# Функция для вывода всей информации об ответе на заявку по её ID
def get_by_id(ticket_id: int) -> TicketResolution | None:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT resolution_id, ticket_id, solution_text
        FROM ticket_resolutions
        WHERE ticket_id = ?
    """, (ticket_id))

    row = cur.fetchone() # Возвращает одну запись из БД
    conn.close()

    return _map(row) if row else None