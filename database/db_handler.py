import os

import psycopg2
from dotenv import load_dotenv
from database.utils import db_config_parser

from models.area import Area
from models.employer import Employer
from models.employment import Employment
from models.experience import Experience
from models.vacancy import Vacancy


class DBHandler:
    db_config = db_config_parser(
        filename="config.ini",
        section="postgres"
    )

    def connect_to_db(self, conn_dbname):
        load_dotenv()
        db_user = os.environ.get("username")
        db_pass = os.environ.get("password")
        host = self.db_config["host"]
        port = self.db_config["port"]
        connection = psycopg2.connect(
            host=host,
            port=port,
            dbname=conn_dbname,
            user=db_user,
            password=db_pass
        )
        return connection

    def __create_database(self, conn_dbname, dbname):
        connection = self.connect_to_db(conn_dbname)
        connection.autocommit = True
        cursor = connection.cursor()

        try:
            cursor.execute(f"DROP DATABASE {dbname} WITH (FORCE)")
        except psycopg2.Error:
            print("База данных не найдена, продолжение работы")
        finally:
            cursor.execute(f"CREATE DATABASE {dbname}")
            print(f"База данных {dbname} создана")

        cursor.close()
        connection.close()

    def create_db_getter(self, conn_dbname, dbname):
        return self.__create_database(conn_dbname, dbname)

    def __create_tables(self, conn_dbname):
        try:
            with self.connect_to_db(conn_dbname) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "CREATE TABLE employer "
                        "("
                        "id INTEGER NOT NULL CONSTRAINT employer_pk PRIMARY KEY,"
                        "name TEXT NOT NULL,"
                        "employer_url TEXT"
                        ")"
                    )

                    cursor.execute(
                        "CREATE TABLE experience "
                        "("
                        "id TEXT NOT NULL CONSTRAINT experience_pk PRIMARY KEY, "
                        "name TEXT NOT NULL"
                        ")"
                    )

                    cursor.execute(
                        "CREATE TABLE employment"
                        "("
                        "id TEXT NOT NULL CONSTRAINT employment_pk PRIMARY KEY, "
                        "name TEXT NOT NULL"
                        ")"
                    )

                    cursor.execute(
                        "CREATE TABLE area"
                        "("
                        "id INTEGER CONSTRAINT area_id_pk PRIMARY KEY,"
                        "name VARCHAR(255)"
                        ")"
                    )

                    cursor.execute(
                        "CREATE TABLE vacancy "
                        "("
                        "id INTEGER NOT NULL CONSTRAINT vacancy_pk PRIMARY KEY,"
                        "name TEXT NOT NULL,"
                        "area_id INTEGER NOT NULL CONSTRAINT area_id_fk REFERENCES area(id),"
                        "salary_from INTEGER NOT NULL,"
                        "salary_to INTEGER NOT NULL,"
                        "vacancy_url TEXT,"
                        "employer_id INTEGER CONSTRAINT employer_fk REFERENCES employer(id),"
                        "requirement TEXT,"
                        "experience_id TEXT CONSTRAINT experience_fk REFERENCES experience(id),"
                        "employment TEXT CONSTRAINT employment_fk REFERENCES employment(id))"
                    )
        finally:
            connection.close()
            print("Созданы таблицы")

    def create_tables_getter(self, conn_dbname):
        return self.__create_tables(conn_dbname)

    def __load_data_to_db(self, conn_dbname):
        area = Area()
        area.instantiate_from_api_data()
        areas = area.all

        employer = Employer()
        employer.instantiate_from_api_data()
        employers = employer.all

        employment = Employment()
        employment.instantiate_from_api_data()
        employments = employment.all

        experience = Experience()
        experience.instantiate_from_api_data()
        experiences = experience.all

        vacancy = Vacancy()
        vacancy.instantiate_form_api_data()
        vacancies = vacancy.all

        try:
            with self.connect_to_db(conn_dbname) as connection:
                with connection.cursor() as cursor:
                    # Добавляем команду TRUNCATE TABLE vacancy; для удаления всех записей из таблицы
                    cursor.execute("TRUNCATE TABLE vacancy;")
                    for item in areas:
                        cursor.execute(
                            "INSERT INTO area VALUES (%s, %s)", (
                                item.id,
                                item.name
                            )
                        )

                    for item in employers:
                        cursor.execute(
                            "INSERT INTO employer VALUES (%s, %s, %s)", (
                                item.id,
                                item.name,
                                item.employer_url
                            )
                        )

                    for item in experiences:
                        cursor.execute(
                            "INSERT INTO experience VALUES (%s, %s)", (
                                item.id,
                                item.name
                            )
                        )

                    for item in employments:
                        cursor.execute(
                            "INSERT INTO employment VALUES (%s, %s)", (
                                item.id,
                                item.name
                            )
                        )

                    for item in vacancies:
                        cursor.execute(
                            "INSERT INTO vacancy VALUES ("
                            "%s, "
                            "%s, "
                            "%s, "
                            "%s, "
                            "%s, "
                            "%s, "
                            "%s, "
                            "%s, "
                            "%s, "
                            "%s"
                            ")",
                            (
                                item.id,
                                item.name,
                                item.area_id,
                                item.salary_from,
                                item.salary_to,
                                item.vacancy_url,
                                item.employer_id,
                                item.requirement,
                                item.experience_id,
                                item.employment
                            )
                        )

        finally:
            connection.close()
            print("Данные загружены")

    def load_data_to_db_getter(self, conn_dbname):
        return self.__load_data_to_db(conn_dbname)