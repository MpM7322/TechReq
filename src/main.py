from techreq.database.techreq_db import init_db
from techreq.services.auth_service import create_default_executor
from auth import login, reg_client, reg_executor
from menu import client_menu, executor_menu

def main():
    init_db()
    create_default_executor()

    while True:
        print("\n╔════════════════════════════════════════╗")
        print("║          ДОБРО ПОЖАЛОВАТЬ В            ║")
        print("║                TECHREQ                 ║")
        print("╚════════════════════════════════════════╝")
        print(" 1. Войти в систему")
        print(" 2. Зарегистрироваться как клиент")
        print(" 0. Выйти из программы")
        print("──────────────────────────────────────────")

        choice = input("Выберите вариант: ").strip()

        if choice == "1":
            user = login()

            if not user:
                continue

            if user.user_role == 2:
                executor_menu(user)
            else:
                client_menu(user)

        elif choice == "2":
            reg_client()

        elif choice == "0":
            print("\nСпасибо за использование TechReq. До свидания!")
            break

        else:
            print("\nНеверный ввод! Пожалуйста, выберите пункт от 0 до 2.")

if __name__ == "__main__":
    main()