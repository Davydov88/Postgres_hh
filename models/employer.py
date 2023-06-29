from api.api_hh import HHAPIHandler


class Employer:
    """
    Класс сущности места работодателя
    """
    all = []

    def __init__(self, id: int = None, name: str = None, employer_url: str = None):
        self.id = id
        self.name = name
        self.employer_url = employer_url
        self.all.append(self)

    @classmethod
    def instantiate_from_api_data(cls):
        """
        Инициализирует экземпляры класса Employer данными из API
        :return: None
        """
        cls.all = []
        api_data_cls = HHAPIHandler()
        data = api_data_cls.get_employer_data()
        for item in data:
            cls(
                item["id"],
                item["name"],
                item["employer_url"]
            )
