from api.api_hh import HHAPIHandler


class Experience:
    """
    Класс сущности опыта работы
    """
    all = []

    def __init__(self, id: str = None, name: str = None):
        self.id = id
        self.name = name
        self.all.append(self)

    @classmethod
    def instantiate_from_api_data(cls):
        """
        Инициализирует экземпляры класса Experience данными из API
        :return: None
        """
        cls.all = []
        api_data_cls = HHAPIHandler()
        data = api_data_cls.get_experience_data()
        for item in data:
            cls(
                item["id"],
                item["name"],
            )
