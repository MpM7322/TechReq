from dataclasses import dataclass

@dataclass
class TicketResolution:
    resolution_id: int
    ticket_id: int
    solution_text: str