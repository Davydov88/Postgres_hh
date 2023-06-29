from api.api_hh import HHAPIHandler


class Vacancy:
    """
    Класс сущности вакансии
    """
    all = []

    def __init__(
            self,
            id: int = None,
            name: str = None,
            area_id: int = None,
            salary_from: int = None,
            salary_to: int = None,
            vacancy_url: str = None,
            employer_id: str = None,
            requirement: str = None,
            experience_id: str = None,
            employment: str = None
    ):
        self.id = id
        self.name = name
        self.area_id = area_id,
        self.salary_from = salary_from,
        self.salary_to = salary_to,
        self.vacancy_url = vacancy_url,
        self.employer_id = employer_id,
        self.requirement = requirement,
        self.experience_id = experience_id,
        self.employment = employment
        self.all.append(self)

    @classmethod
    def instantiate_form_api_data(cls):
        """
        Инициализирует экземпляры класса Vacancy данными из API
        :return: None
        """
        cls.all = []
        api_data_cls = HHAPIHandler()
        data = api_data_cls.get_vacancies_data()
        for item in data:
            if item["salary"]["from"] is None:
                salary_from = item["salary"]["to"]
            else:
                salary_from = item["salary"]["from"]

            if item["salary"]["to"] is None:
                salary_to = item["salary"]["from"]
            else:
                salary_to = item["salary"]["to"]
            cls(
                item["id"],
                item["name"],
                item["area"]["id"],
                salary_from,
                salary_to,
                item["alternate_url"],
                item["employer"]["id"],
                item["snippet"]["requirement"],
                item["experience"]["id"],
                item["employment"]["id"]
            )
