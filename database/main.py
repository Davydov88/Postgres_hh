from prettytable import PrettyTable

from database.db_handler import DBHandler
from database.db_manager import DBManager


def list_menu_items() -> None:
    """
    Выводит в консоль список доступных методов получения данных из БД
    :return: None
    """
    interact_options: list = [
        "Получить список всех компаний и количество вакансий у каждой компании",
        "Получить список всех вакансий с указанием названия компании, "
        "названия вакансии и зарплаты и ссылки на вакансию",
        "Получить среднюю зарплату по вакансиям",
        "Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям",
        "Получить список всех вакансий, в названии которых содержатся переданные в метод слова",
        "Выход из программы"
    ]
    n = 1
    for item in interact_options:
        print(str(n) + ".", item)
        n += 1


def get_user_input() -> int:
    """
    Проверяет, что введеное значение является int
    и находится в переделах диапазона номеров опций из функции list_menu_items()
    :return: введеное пользователем число
    :rtype: int
    """
    while True:
        try:
            option_number = int(input())
            while option_number not in range(1, 7):
                print("Необходимо ввести номер опции (1 - 7)")
                option_number = int(input())
            break
        except ValueError:
            print("Необходимо ввести номер опции (1 - 7)")
    return option_number


def choose_db_manager_method():
    """
    Функция взаимодействия с пользователем
    """
    print("Здравствуйте, доступны следующие операции с базой данных:")
    list_menu_items()
    print("Укажите номер опции для получения результата.")

    db_manager = DBManager()

    option_number = get_user_input()
    while option_number != 6:
        table = PrettyTable()
        if option_number == 1:
            print("Cписок всех компаний и количество вакансий у каждой компании")
            data: list[tuple] = db_manager.get_companies_and_vacancies_count()
            table.field_names = ["Компания", "Кол-во вакансий"]
            for item in data:
                table.add_row([item[0], item[1]])
            print(table)

        elif option_number == 2:
            db_manager.get_all_vacancies()
            print("Список всех вакансий с указанием названия компании,"
                  "названия вакансии и зарплаты и ссылки на вакансию")
            data: list[tuple] = db_manager.get_all_vacancies()
            table.field_names = [
                "Компания",
                "Название вакансии",
                "Зарплата от",
                "Зарплата до",
                "Ссылка на вакансию"
            ]
            for item in data:
                table.add_row(
                    [
                        item[0],
                        item[1],
                        item[2],
                        item[3],
                        item[4]
                    ]
                )
            table.align = "c"
            table.max_width = 60
            print(table)

        elif option_number == 3:
            print("Cредняя зарплата по вакансиям")
            data: tuple = db_manager.get_avg_salary()
            table.header = False
            table.add_row(data[0])
            print(table)

        elif option_number == 4:
            data: list[tuple] = db_manager.get_vacancies_with_higher_salary()
            print("Cписок всех вакансий, у которых зарплата выше средней по всем вакансиям")
            table.field_names = [
                "id",
                "Компания",
                "Название вакансии",
                "Зарплата от",
                "Зарплата до",
                "Ссылка на вакансию"
            ]

            for item in data:
                table.add_row(
                    [
                        item[0],
                        item[1],
                        item[2],
                        item[3],
                        item[4],
                        item[5]
                    ]
                )
            table.align = "c"
            table.max_width = 60
            print(table)

        elif option_number == 5:
            search_keyword = input("Введите слово для поиска\n")
            data: list[tuple] = db_manager.get_vacancies_with_keyword(search_keyword)
            if not len(data) == 0:
                print(f"Cписок всех вакансий, в названии которых содержится слово '{search_keyword}'")
                table.field_names = [
                    "id",
                    "Компания",
                    "Название вакансии",
                    "Зарплата от",
                    "Зарплата до",
                    "Ссылка на вакансию"
                ]

                for item in data:
                    table.add_row(
                        [
                            item[0],
                            item[1],
                            item[2],
                            item[3],
                            item[4],
                            item[5]
                        ]
                    )
                table.align = "c"
                table.max_width = 60
                print(table)
            else:
                print("Вакансии с таким словом в заголовке не найдены")

        list_menu_items()
        option_number = get_user_input()
        continue
    if option_number == 6:
        exit("Программа завершена")


if __name__ == "__main__":
    db_handler = DBHandler()
    db_handler.create_db_getter(conn_dbname="postgres", dbname="hh_vacancies")
    db_handler.create_tables_getter(conn_dbname="hh_vacancies")
    db_handler.load_data_to_db_getter(conn_dbname="hh_vacancies")
    choose_db_manager_method()

