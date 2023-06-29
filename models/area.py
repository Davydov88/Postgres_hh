from api.api_hh import HHAPIHandler


class Area:
    """
    Класс сущности места работы
    """
    all = []

    def __init__(
            self,
            id: int = None,
            name: str = None
    ):
        self.id = id
        self.name = name
        self.all.append(self)

    @classmethod
    def instantiate_from_api_data(cls) -> None:
        """
        Инициализирует экземпляры класса Area данными из API
        :return: None
        """
        cls.all = []
        api_data_cls = HHAPIHandler()
        data: list[dict] = api_data_cls.get_area_data()
        for item in data:
            cls(
                item["id"],
                item["name"]
            )
