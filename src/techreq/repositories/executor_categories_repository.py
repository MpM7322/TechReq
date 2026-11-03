from techreq.database.techreq_db import get_connection
from techreq.models.executor_categories import ExecutorCategories

# Вспомогательная функция преобразования данных
def _map(row) -> ExecutorCategories:
    return ExecutorCategories(*row)

# Функция для добавления сотруднику возможность обрабатывать заявки с определёнными категориями
def allow_ticket_type(executor_id: int, ticket_category_id: int) -> int:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO executor_categories(executor_id, ticket_category_id)
        VALUES (?,?)
    """, (executor_id, ticket_category_id,))

    executor_category = cur.lastrowid

    conn.commit()
    conn.close()

    return executor_category

# Функция для получения всех записей
def get_all() -> list[ExecutorCategories]:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            ec.executor_category_id, 
            ec.executor_id, 
            u.name AS executor_name,
            ec.ticket_category_id,
            c.name AS ticket_category_name
        FROM executor_categories ec
        JOIN users u ON ec.executor_id = u.user_id
        JOIN ticket_categories c ON ec.ticket_category_id = c.category_id
        ORDER BY ec.executor_id
    """)

    rows = cur.fetchall() # Преобразование всех записей в кортежи
    conn.close()

    return [_map(lines) for lines in rows]

# Функция для вывода всех возможностях сотрудника по его ID
def get_by_executor_id(executor_id: int) -> list[ExecutorCategories]:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            ec.executor_category_id, 
            ec.executor_id, 
            u.name AS executor_name,
            ec.ticket_category_id,
            c.name AS ticket_category_name
        FROM executor_categories ec
        JOIN users u ON ec.executor_id = u.user_id
        JOIN ticket_categories c ON ec.ticket_category_id = c.category_id
        WHERE ec.executor_id = ?
    """, (executor_id,))

    rows = cur.fetchall() # Преобразование всех записей в кортежи
    conn.close()

    return [_map(lines) for lines in rows]