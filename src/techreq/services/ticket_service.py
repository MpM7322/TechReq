from techreq.repositories import ticket_repository
from techreq.repositories import ticket_categories_repository
from techreq.repositories import ticket_resolutions_repository
from techreq.repositories import user_repository
from techreq.models.ticket import Ticket

EXECUTOR_ROLE_ID = 2

# Функция для получения категорий
def get_categories() -> list:
    return ticket_categories_repository.get_all()

# Функция для создания заявки
def create_ticket(ticket_description: str, user_id: int, category_id: int) -> Ticket:
    if not ticket_description.strip():
        raise Exception("Описание заявки не может быть пустым!")
    
    if not user_id:
        raise Exception("ID пользователя не может быть пустым!")

    if not user_repository.get_by_id(user_id):
        raise Exception(f"Пользователя с ID = {user_id} не существует! Необходима регистрация!")
    
    categories = ticket_categories_repository.get_all()
    valid_ids = [cat.category_id for cat in categories]
    if category_id not in valid_ids:
        raise Exception("Категории заявки с таким ID не существует!")

    ticket_id = ticket_repository.create(category_id, ticket_description, user_id)
    return ticket_repository.get_by_id(ticket_id)

# Функция для удаления заявки
def delete_ticket(ticket_id: int) -> bool:
    if not ticket_id:
        raise Exception("ID заявки не может быть пустым!")

    ticket = ticket_repository.get_by_id(ticket_id)
    if not ticket:
        raise Exception(f"Заявка с ID = {ticket_id} не найдена!")

    ticket_repository.delete_ticket(ticket_id)
    return True
        
# Функция для просмотра заявок пользователя по его ID
def get_tickets_by_user_id(user_id: int) -> list[Ticket]:
    if not user_id:
        raise Exception("ID пользователя не может быть пустым!")

    if not user_repository.get_by_id(user_id):
        raise Exception(f"Пользователя с ID = {user_id} не существует! Необходима регистрация!")

    all_tickets = ticket_repository.get_all()
    user_tickets = [ticket for ticket in all_tickets if ticket.user_id == user_id]

    return user_tickets

# Функция для назначения к заявке сотрудника
def set_executor(ticket_id: int, executor_id: int) -> Ticket:
    if not ticket_id:
        raise Exception("ID заявки не может быть пустым!")

    if not executor_id:
        raise Exception("ID сотрудник не может быть пустым!")

    ticket = ticket_repository.get_by_id(ticket_id)
    if not ticket:
        raise Exception(f"Заявка с ID = {ticket_id} не найдена!")

    executor = user_repository.get_by_id(executor_id)
    if not executor:
        raise Exception(f"Пользователя с ID = {executor_id} не существует! Необходима регистрация!")

    if executor.user_role != EXECUTOR_ROLE_ID:
        raise Exception(f"Пользователь с ID = {executor_id} не является сотрудником! Назначение невозможно!")

    ticket_repository.set_executor(ticket_id, executor_id)

    return ticket_repository.get_by_id(ticket_id)

# Функция для ответа на заявку
def answer_ticket(ticket_id: int, executor_id: int, solution_text: str) -> Ticket:
    if not ticket_id:
        raise Exception("ID заявки не может быть пустым!")

    if not executor_id:
        raise Exception("ID сотрудника не может быть пустым!")

    if not solution_text.strip():
        raise Exception("Текст ответа на заявку не может быть пустым!")

    ticket = ticket_repository.get_by_id(ticket_id)
    if not ticket:
        raise Exception(f"Заявка с ID = {ticket_id} не найдена!")

    if ticket.executor_id is None:
        raise Exception("На эту заявку ещё не назначен сотрудник! Сначала назначьте его!")

    if ticket.executor_id != executor_id:
        raise Exception("Вы не можете ответить на эту заявку, на неё назначен другой сотрудник!")

    ticket_resolutions_repository.answer_ticket(ticket_id, solution_text)
    ticket_repository.update_ticket_status(ticket_id)

    return ticket_repository.get_by_id(ticket_id)

# Функция для получения всех свободных заявок
def get_free_tickets() -> list[Ticket]:
    all_tickets = ticket_repository.get_all()
    free = [ticket for ticket in all_tickets if ticket.executor_id is None]
    return free

# Фукнция для просмотра заявок, прикреплённых к определённому сотруднику
def get_tickets_by_executor_id(executor_id: int) -> list[Ticket]:
    if not executor_id:
        raise Exception("ID пользователя не может быть пустым!")

    executor = user_repository.get_by_id(executor_id)
    if not executor:
        raise Exception(f"Пользователя с ID = {executor_id} не существует! Необходима регистрация!")

    if executor.user_role != EXECUTOR_ROLE_ID:
        raise Exception(f"Пользователь с ID = {executor_id} не является сотрудником! Просмотр его заявок невозможен!")