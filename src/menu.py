from techreq.services import ticket_service
from techreq.services import executor_service

from auth import reg_executor

# Меню сотруднкиа
def executor_menu(user):

    while True:
        print("\n╔════════════════════════════════════════╗")
        print(f"║     ПАНЕЛЬ УПРАВЛЕНИЯ СОТРУДНИКА       ║")
        print(f"║     Логин: {user.login:<27} ║")
        print("╚════════════════════════════════════════╝")
        print(" 1. Посмотреть свободные заявки")
        print(" 2. Взять заявку в работу")
        print(" 3. Мои заявки в работе")
        print(" 4. Ответить на заявку")
        print(" 5. Список всех клиентов")
        print(" 6. Список всех сотрудников")
        print(" 7. Посмотреть статистику системы")
        print(" 8. Удалить заявку")
        print(" 9. Зарегистрировать нового сотрудника")
        print(" 0. Выход")
        print("──────────────────────────────────────────")

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            tickets = ticket_service.get_free_tickets()
            if not tickets:
                print("\nСвободных заявок нет!")
                continue
            print("\nСписок свободных заявок:")
            print("──────────────────────────────────────────")
            for t in tickets:
                print(f" ID: {t.ticket_id} | Категория: {t.ticket_category_name} | Описание: {t.ticket_description}")
            print("──────────────────────────────────────────")


        elif choice == "2":
            ticket_id = input("Введите ID заявки, чтобы взять её в работу: ").strip()
            if not ticket_id.isdigit():
                print("\nОшибка: ID должен быть числом!")
                continue
            try:
                ticket_service.set_executor(int(ticket_id), user.user_id)
                print(f"\nВы успешно назначены исполнителем заявки №{ticket_id}!")
            except Exception as e:
                print(f"\nОшибка: {e}")


        elif choice == "3":
            try:
                tickets = ticket_service.get_tickets_by_executor_id(user.user_id)
                if not tickets:
                    print("\nУ вас нет активных заявок в работе.")
                    continue
                print("\nЗаявки у вас в работе:")
                print("──────────────────────────────────────────")
                for t in tickets:
                    print(f" ID: {t.ticket_id} | Категория: {t.ticket_category_name} | Описание: {t.ticket_description}")
                print("──────────────────────────────────────────")
            except Exception as e:
                print(f"\nОшибка: {e}")


        elif choice == "4":
            ticket_id = input("Введите ID заявки для ответа: ").strip()
            solution_text = input("Введите текст ответа (решение): ").strip()
            if not ticket_id.isdigit():
                print("\nОшибка: ID должен быть числом!")
                continue
            try:
                ticket_service.answer_ticket(int(ticket_id), user.user_id, solution_text)
                print(f"\nОтвет на заявку №{ticket_id} успешно отправлен!")
            except Exception as e:
                print(f"\nОшибка: {e}")

       
        elif choice == "5":
            clients = executor_service.get_all_clients()
            if not clients:
                print("\nКлиенты не найдены.")
                continue
            print("\nСписок всех клиентов:")
            print("──────────────────────────────────────────")
            for c in clients:
                print(f" ID: {c.user_id} | Логин: {c.login} | ФИО: {c.surname} {c.name} {c.patronymic}")
            print("──────────────────────────────────────────")


        elif choice == "6":
            executors = executor_service.get_all_executors()
            print("\nСписок всех сотрудников:")
            print("──────────────────────────────────────────")
            for e in executors:
                print(f" ID: {e.user_id} | Логин: {e.login} | ФИО: {e.surname} {e.name} {e.patronymic}")
            print("──────────────────────────────────────────")


        elif choice == "7":
            stats = executor_service.get_system_stats()
            print("\nСтатистика системы:")
            print("──────────────────────────────────────────")
            for key, value in stats.items():
                print(f" {key}: {value}")
            print("──────────────────────────────────────────")


        elif choice == "8":
            ticket_id = input("Введите ID заявки для удаления: ").strip()
            if not ticket_id.isdigit():
                print("\nОшибка: ID должен быть числом!")
                continue
            try:
                ticket_service.delete_ticket(int(ticket_id))
                print(f"\nЗаявка №{ticket_id} успешно удалена!")
            except Exception as e:
                print(f"\nОшибка: {e}")


        elif choice == "9":
            reg_executor()

        elif choice == "0":
            print("\nВыход из панели управления...")
            break

        else:
            print("\nНеверный пункт меню!") 

def client_menu(user):

    while True:
        print("\n╔════════════════════════════════════════╗")
        print(f"║     ЛИЧНЫЙ КАБИНЕТ КЛИЕНТА             ║")
        print(f"║     Логин: {user.login:<27} ║")
        print("╚════════════════════════════════════════╝")
        print(" 1. Создать новую заявку")
        print(" 2. Посмотреть мои заявки")
        print(" 0. Выйти из аккаунта")
        print("──────────────────────────────────────────")

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            print("\nДоступные категории заявок:")
            try:
                categories = ticket_service.get_categories()
                for cat in categories:
                    print(f" [{cat.category_id}] {cat.name}")
                
                category_id = input("\nВведите ID категории: ").strip()
                description = input("Введите описание вашей проблемы: ").strip()

                if not category_id.isdigit():
                    print("\nОшибка: ID категории должен быть числом!")
                    continue

                new_ticket = ticket_service.create_ticket(description, user.user_id, int(category_id))
                print(f"\nЗаявка №{new_ticket.ticket_id} успешно создана! Ожидайте ответа.")
            except Exception as e:
                print(f"\nОшибка: {e}")


        elif choice == "2":
            try:
                tickets = ticket_service.get_tickets_by_user_id(user.user_id)
                if not tickets:
                    print("\nУ вас пока нет созданных заявок.")
                    continue

                print("\nВаши заявки:")
                print("──────────────────────────────────────────")
                for t in tickets:
                    print(f" ID: {t.ticket_id} | Категория: {t.ticket_category_name}")
                    print(f" Описание: {t.ticket_description}")
                    print(f" Статус: {t.current_status_name}")
                    
                    # ПРОВЕРЯЕМ: Если статус "Получен ответ" или поле ответа не пустое — выводим его
                    # (Замените t.ticket_resolution_solution_text на ваше точное имя поля из модели Ticket, если оно другое)
                    if getattr(t, 'ticket_resolution_solution_text', None):
                        print(f" Ответ сотрудника: {t.ticket_resolution_solution_text}")
                    elif getattr(t, 'solution_text', None):
                        print(f" Ответ сотрудника: {t.solution_text}")
                        
                    print("──────────────────────────────────────────")
            except Exception as e:
                print(f"\nОшибка: {e}")

        elif choice == "0":
            print("\nВыход из личного кабинета...")
            break

        else:
            print("\nНеверный пункт меню!")