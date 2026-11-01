from src.techreq.database.techreq_db import get_connection
from src.techreq.models.executor_categories import ExecutorCategories

# Вспомогательная функция преобразования данных
def _map(row) -> ExecutorCategories:
    return ExecutorCategories(*row)

# Функция для добавления сотруднику возможность обрабатывать заявки с определёнными категориями
def allow_ticket_type(executor_id: int, ticket_category_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO executor_categories(executor_id, ticket_category_id)
        VALUES (? ?)
    """, (executor_id, ticket_category_id))

    conn.commit()
    conn.close()

# Функция для получения всех записей
def get_all() -> list[ExecutorCategories]:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT executor_category_id, executor_id, ticket_category_id
        FROM executor_categories
        ORDER BY executor_id
    """)

    rows = cur.fetchall() # Преобразование всех записей в кортежи
    conn.close()

    return [_map(lines) for lines in rows]

# Функция для вывода всех возможностях сотрудника по его ID
def get_by_executor_id(executor_id: int) -> ExecutorCategories | None:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT executor_category_id, executor_id, ticket_category_id
        FROM executor_categories
        WHERE executor_id = ?
    """, (executor_id))

    row = cur.fetchone() # Возвращает одну запись из БД
    conn.close()

    return _map(row) if row else None