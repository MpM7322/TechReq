from dataclasses import dataclass

@dataclass
class User:
    user_id: int
    name: str
    surname: str
    patronymic: str
    login: str
    password: str
    user_role: int

    user_role_name: str | None = None