from dataclasses import dataclass

@dataclass
class Ticket:
    ticket_id: int
    ticket_category_id: int
    ticket_description: str
    current_status_id: int
    user_id: int
    executor_id: int

    ticket_category_name: str | None = None
    current_status_name: str | None = None
