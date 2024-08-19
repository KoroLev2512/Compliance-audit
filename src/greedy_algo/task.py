class Task:
    def __str__(self):
        """
        Возвращает строковое представление объекта класса Task в виде строки.
        Строка включает имя задачи, продолжительность и тему задачи.
        """
        return f'|{self.name=}, {self.duration=}, {self.theme=}|'

    def __repr__(self):
        """
        Возвращает строковое представление объекта класса Task в виде строки.
        Используется для представления объекта в интерактивных оболочках и логировании.
        """
        return f'|{self.name=}, {self.duration=}, {self.theme=}|'

    def __init__(self, name, duration, theme: int):
        """
        Инициализирует объект класса Task.

        Аргументы:
        name (str): Имя задачи.
        duration (int): Продолжительность выполнения задачи (время в часах, минутах или другом формате).
        theme (int): Тема задачи, к которой она относится.
        """
        self.name = name
        self.duration = duration
        self.theme = theme
