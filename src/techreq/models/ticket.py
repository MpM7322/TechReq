from dataclasses import dataclass

@dataclass
class Ticket:
    ticket_id: int
    ticket_category_id: int
    ticket_category_name: str | None
    current_status_id: int
    current_status_name: str | None
    user_id: int
    executor_id: int | None
    ticket_description: str
    ticket_resolution_solution_text: str | None = None
