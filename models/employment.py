from api.api_hh import HHAPIHandler


class Employment:
    """
    Класс сущности типа занятости
    """
    all = []

    def __init__(self, id: int = None, name: str = None):
        self.id = id
        self.name = name
        self.all.append(self)

    @classmethod
    def instantiate_from_api_data(cls):
        """
        Инициализирует экземпляры класса Employment данными из API
        :return: None
        """
        cls.all = []
        api_data_cls = HHAPIHandler()
        data = api_data_cls.get_employment_data()
        for item in data:
            cls(
                item["id"],
                item["name"],
            )
            