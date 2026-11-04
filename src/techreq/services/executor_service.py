from techreq.repositories import user_repository
from techreq.repositories import ticket_repository
from techreq.models.user import User

CLIENT_ROLE_ID = 1
EXECUTOR_ROLE_ID = 2


# Фукнция для получения всех клиентов
def get_all_clients() -> list[User]:
    all_users = user_repository.get_all()
    return [user for user in all_users if user.user_role == CLIENT_ROLE_ID]

# Фукнция для получения всех сотрудников
def get_all_executors() -> list[User]:
    all_users = user_repository.get_all()
    return [user for user in all_users if user.user_role == EXECUTOR_ROLE_ID]

# Функция для получения статистики системы
def get_system_stats() -> dict:
    all_tickets = ticket_repository.get_all()
    all_users = user_repository.get_all()

    new_tickets = len([ticket for ticket in all_tickets if ticket.current_status_id == 1])
    closed_tickets = len([ticket for ticket in all_tickets if ticket.current_status_id == 2])

    stats = {
        "Всего пользователей": len(all_users),
        "Всего клиентов": len([user for user in all_users if user.user_role == CLIENT_ROLE_ID]),
        "Всего сотрудников": len([user for user in all_users if user.user_role == EXECUTOR_ROLE_ID]),
        "Всего заявок": len(all_tickets),
        "Всего заявок, которые ожидают ответа": len(new_tickets),
        "Всего заявок, которые получили ответ": len(closed_tickets)
    }
    return stats

