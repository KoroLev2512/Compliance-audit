class Theme:
    def __str__(self):
        """
        Возвращает строковое представление объекта класса Theme.
        Представление включает имя темы, список задач и список работников, связанных с этой темой.
        """
        return f'{self.name=}, {self.tasks=}, {self.workers=}'

    def __init__(self, name: int, tasks):
        """
        Инициализирует объект класса Theme.

        Аргументы:
        name (int): Имя или идентификатор темы.
        tasks (list): Список задач, относящихся к данной теме.
        """
        self.name = name
        self.tasks = tasks
        self.workers = []

    def add_worker(self, worker):
        """
        Добавляет работника к теме.

        Аргументы:
        worker (Worker): Работник, которого необходимо добавить к теме.
        """
        self.workers.append(worker)

    def remove_worker(self, worker):
        """
        Удаляет работника из темы.

        Аргументы:
        worker (Worker): Работник, которого необходимо удалить из темы.
        """
        self.workers.remove(worker)
