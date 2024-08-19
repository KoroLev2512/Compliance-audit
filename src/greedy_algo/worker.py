class Worker:
    def __repr__(self):
        """
        Возвращает строковое представление объекта класса Worker.
        Представление включает имя, текущую задачу, историю задач и эффективность по темам.
        """
        return f'|{self.name=}, {self.current_task=}, {self.history=}, {self.themes_efficiency=}|\n'

    def __init__(self, name, history: list, current_task, themes_efficiency, is_president=False):
        """
        Инициализирует объект класса Worker.

        Аргументы:
        name (str): Имя работника.
        history (list): История задач, выполненных работником.
        current_task (str): Текущая задача, над которой работает работник.
        themes_efficiency (dict): Словарь, где ключами являются темы задач, а значениями — оперативность работника в данной теме.
        is_president (bool): Указывает, является ли работник председателем (по умолчанию False).
        """
        self.name = name
        self.history = history
        self.current_task = current_task
        self.themes_efficiency = themes_efficiency
        self.is_president = is_president
