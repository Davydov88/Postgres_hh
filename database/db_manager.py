from database.db_handler import DBHandler
import psycopg2


class DBManager(DBHandler):

    def get_companies_and_vacancies_count(self) -> list[tuple]:
        """
        Получает список всех компаний
        и количество вакансий у каждой компании
        :return: список кортежей, содержащий данные о компании и количестве вакансий
        :rtype: list[tuple]
        """
        try:
            with self.connect_to_db(conn_dbname="hh_vacancies") as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT employer.name as employer, count(vacancy.id) "
                        "FROM vacancy "
                        "INNER JOIN employer ON employer_id = employer.id "
                        "GROUP BY employer ORDER BY count(employer_id) DESC"
                    )
                    vacancies_data: list[tuple] = cursor.fetchall()
                    return vacancies_data
        finally:
            connection.close()

    def get_all_vacancies(self) -> list[tuple]:
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию.
        :return: список кортежей, содержащий данные о компании и количестве вакансий
        :rtype: list[tuple]
        """
        try:
            with self.connect_to_db(conn_dbname="hh_vacancies") as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT employer.name as employer_name, "
                        "vacancy.name, "
                        "salary_from, "
                        "salary_to, "
                        "vacancy_url "
                        "FROM vacancy "
                        "INNER JOIN employer "
                        "ON vacancy.employer_id = employer.id "
                        "ORDER BY employer_name "
                    )
                    vacancies_data: list[tuple] = cursor.fetchall()
                    return vacancies_data
        finally:
            connection.close()

    def get_avg_salary(self) -> tuple:
        """
        Получает среднюю зарплату по вакансиям.
        return: кортеж, содержащий данные о средней зарплате по всем вакансиям
        :rtype: tuple
        """
        try:
            with self.connect_to_db(conn_dbname="hh_vacancies") as connecton:
                with connecton.cursor() as cursor:
                    cursor.execute(
                        "SELECT "
                        "ROUND (AVG(salary_from)) "
                        "FROM vacancy "
                    )
                    avg_salary_data = cursor.fetchall()
                    return avg_salary_data
        finally:
            connecton.close()

    def get_vacancies_with_higher_salary(self) -> list[tuple]:
        """
        Получает список всех вакансий,
        у которых зарплата выше средней по всем вакансиям.
        :return: список кортежей, содержащий данные о вакансиях
        :rtype: list[tuple]
        """
        try:
            with self.connect_to_db(conn_dbname="hh_vacancies") as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT vacancy.id, employer.name as employer_name, "
                        "vacancy.name, "
                        "salary_from, "
                        "salary_to, "
                        "vacancy_url "
                        "FROM vacancy "
                        "INNER JOIN employer "
                        "ON vacancy.employer_id = employer.id "
                        "WHERE salary_from > (%s) "
                        "ORDER BY employer_name ",
                        (self.get_avg_salary())
                    )
                    vacancies_data = cursor.fetchall()
                    return vacancies_data
        finally:
            connection.close()

    def get_vacancies_with_keyword(self, search_keyword: str) -> list[tuple]:
        """
        Получает список всех вакансий,
        в названии которых содержатся переданные в метод слова
        :param search_keyword: ключевое слово для поиска в названии вакансии
        :type search_keyword: str
        :return: список кортежей, содержащий данные о вакансиях
        :rtype: list[tuple]
        """
        try:
            with self.connect_to_db(conn_dbname="hh_vacancies") as connection:
                with connection.cursor() as cursor:
                    query = 'SELECT vacancy.id, employer.name as employer_name,' \
                            'vacancy.name, ' \
                            'salary_from, ' \
                            'salary_to, ' \
                            'vacancy_url ' \
                            'FROM vacancy ' \
                            'INNER JOIN employer ' \
                            'ON vacancy.employer_id = employer.id ' \
                            'WHERE vacancy.name LIKE (%s)'
                    param_format = '%{}%'.format(search_keyword)
                    cursor.execute(query, (param_format,))
                    vacancies_data = cursor.fetchall()
                    return vacancies_data
        finally:
            connection.close()
