from techreq.database.techreq_db import get_connection
from techreq.models.ticket import Ticket

# Вспомогательная функция преобразования данных
def _map(row) -> Ticket:
    return Ticket(*row)

# Функция для создания заявки
def create(ticket_category_id: int, ticket_description: str, user_id: int) -> int:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO tickets(ticket_category_id, ticket_description, current_status_id, user_id, executor_id)
        VALUES (?, ?, 1, ?, NULL)
    """, (ticket_category_id, ticket_description, user_id,))

    ticket_id = cur.lastrowid

    conn.commit()
    conn.close()

    return ticket_id

# Функция для вывода всей информации о заявке по ID
def get_by_id(ticket_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            t.ticket_id, 
            t.ticket_category_id, 
            c.name AS ticket_category_name,
            t.current_status_id, 
            s.name AS ticket_status_name,
            t.user_id, 
            t.executor_id,
            t.ticket_description,
            r.solution_text AS ticket_resolution_solution_text
        FROM tickets t
        JOIN ticket_categories c ON t.ticket_category_id = c.category_id
        JOIN ticket_status s ON t.current_status_id = s.ticket_status_id
        LEFT JOIN ticket_resolutions r ON t.ticket_id = r.ticket_id 
        WHERE t.ticket_id = ? 
    """, (ticket_id,))

    row = cur.fetchone() # Возвращает одну запись из БД
    conn.close()

    return _map(row) if row else None

# Функция для вывода всех заявок, которые обрабатывает выбранный сотрудник
def get_by_executor_id(executor_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            t.ticket_id, 
            t.ticket_category_id, 
            c.name AS ticket_category_name,
            t.current_status_id, 
            s.name AS ticket_status_name,
            t.user_id, 
            t.executor_id,
            t.ticket_description,
            r.solution_text AS ticket_resolution_solution_text
        FROM tickets t
        JOIN ticket_categories c ON t.ticket_category_id = c.category_id
        JOIN ticket_status s ON t.current_status_id = s.ticket_status_id
        LEFT JOIN ticket_resolutions r ON t.ticket_id = r.ticket_id 
        WHERE t.executor_id = ? 
    """, (executor_id,))

    rows = cur.fetchall() # Преобразование всех записей в кортежи
    conn.close()

    return [_map(lines) for lines in rows]

# Функция для вывода всех заявок
def get_all() -> list[Ticket]:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            t.ticket_id, 
            t.ticket_category_id, 
            c.name AS ticket_category_name,
            t.current_status_id, 
            s.name AS ticket_status_name,
            t.user_id, 
            t.executor_id,
            t.ticket_description,
            r.solution_text AS ticket_resolution_solution_text
        FROM tickets t
        JOIN ticket_categories c ON t.ticket_category_id = c.category_id
        JOIN ticket_status s ON t.current_status_id = s.ticket_status_id
        LEFT JOIN ticket_resolutions r ON t.ticket_id = r.ticket_id 
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
    """, (executor_id, ticket_id,))

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
    """, (ticket_id,))

    conn.commit()
    conn.close()

# Функция для удаления заявки
def delete_ticket(ticket_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM tickets
        WHERE ticket_id = ?
    """, (ticket_id,))

    conn.commit()
    conn.close()