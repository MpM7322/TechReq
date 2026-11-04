from techreq.services.auth_service import (
    authenticate,
    register_client,
    register_executor
)

def login():
    print("\n╔════════════════════════════════════════╗")
    print("║              АВТОРИЗАЦИЯ               ║")
    print("╚════════════════════════════════════════╝")

    login = input(" Логин: ").strip()
    password = input(" Пароль: ").strip()

    user = authenticate(login, password)

    if not user:
        print("\nНеверный логин или пароль!")
        return None

    print(f"\nДобро пожаловать, {user.name}  {user.surname}!")
    return user

def reg_client():
    print("\n╔════════════════════════════════════════╗")
    print("║           РЕГИСТРАЦИЯ КЛИЕНТА          ║")
    print("╚════════════════════════════════════════╝")

    name = input(" Введите ваше имя: ").strip()
    surname = input(" Введите вашу фамилию: ").strip()
    patronymic = input(" Введите ваше отчество: ").strip()
    login = input(" Придумайте логин: ").strip()
    password = input(" Придумайте пароль: ").strip()

    try:
        register_client(name, surname, patronymic, login, password)
        print("\nРегистрация успешна! Теперь вы можете войти!")
    except Exception as e:
        print(f"\nОшибка регистрации: {e}")

def reg_executor():
    print("\n╔════════════════════════════════════════╗")
    print("║         РЕГИСТРАЦИЯ СОТРУДНИКА         ║")
    print("╚════════════════════════════════════════╝")

    name = input(" Имя: ").strip()
    surname = input(" Фамилия: ").strip()
    patronymic = input(" Отчество: ").strip()
    login = input(" Логин: ").strip()
    password = input(" Пароль: ").strip()

    try:
        register_executor(name, surname, patronymic, login, password)
        print("\nСотрудник успешно добавлен в систему!")
    except Exception as e:
        print(f"\nОшибка создания сотрудника: {e}")