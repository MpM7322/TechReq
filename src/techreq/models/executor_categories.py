from dataclasses import dataclass

@dataclass
class ExecutorCategories:
    executor_category_id: int
    executor_id: int
    ticket_category_id: int

    ticket_category_name: str | None = None