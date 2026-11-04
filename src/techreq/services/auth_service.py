from techreq.models.user import User
from techreq.repositories import user_repository
import hashlib

CLIENT_ROLE_ID = 1
EXECUTOR_ROLE_ID = 2

# Функция хэширования пароля
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# Функция входа в систему
def authenticate(login: str, password: str)-> User | None:
    login = login.strip()
    password = password.strip()

    if not login or not password: return None

    user = user_repository.get_by_login(login)
    if not user or user.password_hash != hash_password(password): return None

    return user

# Функция регистрации клиента
def register_client(
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
        raise Exception(f"Клиент с логином {login} уже существует")

    hashed_password = hash_password(password)

    # Создаём в БД нашего клиента, ф-я user_repository.create возвращает id, только что созданного клиента 
    client_id = user_repository.create(name, surname, patronymic, login, hashed_password, CLIENT_ROLE_ID)

    return client_id

# Функция регистрации сотрудника
def register_executor(
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
        raise Exception(f"Сотрудник с логином {login} уже существует")

    hashed_password = hash_password(password)

    # Создаём в БД нашего клиента, ф-я user_repository.create возвращает id, только что созданного клиента 
    executor_id = user_repository.create(name, surname, patronymic, login, hashed_password, EXECUTOR_ROLE_ID)

    return executor_id

# Функция создания первоначального сотрудника
def create_default_executor():
    if user_repository.get_by_login("admin"):
        return

    hashed_password = hash_password("secretpassword")

    user_repository.create(
        "Матвей",
        "Андрюков",
        "Викторович",
        "admin",
        hashed_password,
        EXECUTOR_ROLE_ID
    )