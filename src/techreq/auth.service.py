from repositories import user_repository

CLIENT_ROLE_ID = 1
EXECUTOR_ROLE_ID = 2

def register_user(
    name: str,
    surname: str,
    patronymic: str,
    login: str,
    password: str,
) -> int:
    name = name.strip()
    surname = surname.strip()
    patronymic = patronymic.strip()
    login = login.strip()
    password = password.strip()

    if not name: raise Exception("Имя не может быть пустым!")
    if not surname: raise Exception("Фамилия не может быть пустой!")
    if not patronymic: raise Exception("Отчество не может быть пустым!")
    if not login: raise Exception("Логин не может быть пустым!")
    if not password: raise Exception("Пароль не может быть пустым!")

    if user_repository.get_by_login(login): 
        raise Exception(f"Пользователь с логином {login} уже существует")

    user_id = user_repository.create()