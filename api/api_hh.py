import json
import requests
from api.api_abc_class import APIHandlerABCClass


class HHAPIHandler(APIHandlerABCClass):
    """
    Класс получения данных по API
    """

    @staticmethod
    def get_vacancies_data() -> list[dict]:
        """
        Метод получения всех вакансий по id компаний,
        указанных в пармаретах запроса
        :return: список словарей со всеми вакансиями компаний
        :rtype: list[dict]
        """
        params = {
            "per_page": 100,  # указание количества вакансий на страницу
            "page": 0,  # запрос начинается с нулевой страницы
            "period": 30,  # период размещения вакансий от текущей даты
            "only_with_salary": True,  # возвращать вакансии только с зарплатой
            "area": 113,  # страна поиска Россия
            "search_field": "name",  # в какой обаласти вакансии
            "employer_id": [
                "3809",
                "78638",
                "1740",
                "3776",
                "3127",
                "3529",
                "2104700",
                "15478",
                "4949",
                "2180"
            ]
        }

        response = requests.get("https://api.hh.ru/vacancies", params=params)
        if not response.status_code == 200:
            print(response.status_code, response.text)
        vacancies_description = response.json()["items"]

        # получение количества страниц из ответа
        pages = response.json()["pages"]

        # обновление номера страницы в запросе к API
        for page in range(1, pages):
            params["page"] = page
            response = requests.get(
                "https://api.hh.ru/vacancies",
                params=params
            )
            vacancies_description.extend(response.json()["items"])

        return vacancies_description

    @staticmethod
    def get_employer_data() -> list[dict]:
        """
        Метод получения id, названия, url всех работодателей
        :return: список словарей с данными работодателей
        :rtype: list[dict]
        """
        eid_list: list = [
            "3809",
            "78638",
            "1740",
            "3776",
            "3127",
            "3529",
            "2104700",
            "15478",
            "4949",
            "2180"
        ]
        employer_data = []
        for eid in eid_list:
            response = requests.get(f"https://api.hh.ru/employers/{eid}")
            if not response.status_code == 200:
                print(response.status_code, response.text)
            employer = {
                "id": eid,
                "name": response.json()["name"],
                "employer_url": response.json()["alternate_url"]
            }
            employer_data.append(employer)
        return employer_data

    def get_area_data(self) -> list[dict]:
        """
        Метод получения всех локация работоталей из данных всех вакансий
        :return: Список словарей с локациями работотаделей
        :rtype: list[dict]
        """
        response = requests.get("https://api.hh.ru/areas/113")
        if not response.status_code == 200:
            print(response.status_code, response.text)

        area_list = []
        # страна
        country = {
                "id": response.json()["id"],
                "name": response.json()["name"]
            }
        area_list.append(country)

        # область
        for item in response.json()["areas"]:
            region = {
                "id": item["id"],
                "name": item["name"]
            }
            if region not in area_list:
                area_list.append(region)
            else:
                pass

        # город
        for region in response.json()["areas"]:
            for item in region["areas"]:
                city = {
                    "id": item["id"],
                    "name": item["name"]
                }
                if city not in area_list:
                    area_list.append(city)
                else:
                    pass
        return area_list

    @staticmethod
    def get_additional_dicts() -> dict:
        """
        Метод получения дополнительных справочников по API
        :return: словарь с дополнительными справочниками
        :rtype: dict
        """
        response = requests.get("https://api.hh.ru/dictionaries")
        if not response.status_code == 200:
            print(response.status_code, response.text)
        return response.json()

    def get_experience_data(self) -> list[dict]:
        """
        Метод получения справоничка опыта соискателя
        :return: словарь с данными возможных значений опыта
        :rtype: list[dict]
        """
        data: dict = self.get_additional_dicts()
        experience_data = data["experience"]
        return experience_data

    def get_employment_data(self) -> list[dict]:
        """
        Метод получения справоничка типа работы
        :return: словарь с данными возможных значений типов работы
        :rtype: list[dict]
        """
        data: dict = self.get_additional_dicts()
        employment_data = data["employment"]
        return employment_data
