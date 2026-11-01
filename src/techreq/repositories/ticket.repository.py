from src.techreq.database.techreq_db import get_connection
from src.techreq.models.ticket import Ticket

# Вспомогательная функция преобразования данных
def _map(row) -> Ticket:
    return Ticket(*row)

# Функция для создания заявки
def create(ticket_category_id: int, ticket_description: str, user_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO tickets(ticket_category_id, ticket_description, current_status_id, user_id, executor_id)
        VALUES (?, ?, 1, ?, NULL)
    """, (ticket_category_id, ticket_description, user_id))

    conn.commit()
    conn.close()

# Функция для вывода всей информации о заявке по ID
def get_by_id(ticket_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT ticket_id, ticket_category_id, ticket_description, current_status_id, user_id, executor_id
        FROM tickets
        WHERE ticket_id = ? 
    """, (ticket_id))

    row = cur.fetchone() # Возвращает одну запись из БД
    conn.close()

    return _map(row) if row else None

# Функция для вывода всех заявок, которые обрабатывает выбранный сотрудник
def get_by_executor_id(executor_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT ticket_id, ticket_category_id, ticket_description, current_status_id, user_id, executor_id
        FROM tickets
        WHERE executor_id = ? 
    """, (executor_id))

    row = cur.fetchone() # Возвращает одну запись из БД
    conn.close()

    return _map(row) if row else None

# Функция для вывода всех заявок
def get_all() -> list[Ticket]:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT ticket_id, ticket_category_id, ticket_description, current_status_id, user_id, executor_id
        FROM tickets
    """)

    rows = cur.fetchall() # Преобразование всех записей в кортежи
    conn.close()

    return [_map(lines) for lines in rows]

# Функция для назначения сотрудника к определённой заявке
def set_executor(ticket_id: int, executor_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE tickets
        SET executor_id = ?
        WHERE ticket_id = ?
    """, (executor_id, ticket_id))

    conn.commit()
    conn.close()

# Функция для изменения статуса заявки, в случае если на неё ответили
def update_ticket_status(ticket_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE tickets
        SET current_status_id = 2
        WHERE ticket_id = ?
    """, (ticket_id))

    conn.commit()
    conn.close()

# Функция для удаления заявки
def delete_ticket(ticket_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM tickets
        WHERE ticket_id = ?
    """, (ticket_id))

    conn.commit()
    conn.close()