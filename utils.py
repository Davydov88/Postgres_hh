from configparser import ConfigParser


def db_config_parser(filename: str, section: str) -> dict:
    """
    Получает конфиги из файла и сохраняет их в словарь
    :param filename: имя конфиг-файла
    :type filename: str
    :param section: раздел с конфигами в файле
    :type section: str
    :return: словарь с данными конфигурации из заданного раздела файла
    :rtype: dict
    """
    parser = ConfigParser()
    parser.read(filename)
    db_config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db_config[param[0]] = param[1]
    else:
        raise Exception(
            f"Раздел {section} не найден в файле {filename}"
        )
    return db_config