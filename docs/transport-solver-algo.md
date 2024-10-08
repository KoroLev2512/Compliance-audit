# Transportation Problem Solver

## Описание решения

Этот проект представляет собой программу для решения транспортной задачи линейного программирования открытого типа. Программа позволяет добавлять фиктивных исполнителей и события, а затем оптимизирует количество времени, затрачиваемого каждым исполнителем на каждую тему, с использованием метода северо-западного угла. Подробное описание теории и пошагового решения можно найти в [статье на Хабре](https://habr.com/ru/articles/573224/).

## Требования к среде разработки

- **IDE:** PyCharm Community Edition 2024.1
- **Язык программирования:** Python 3.12
- **Библиотеки и их версии:**

    1. click==8.0.3
    2. colorama==0.4.4
    3. Flask==2.0.2
    4. Flask-WTF==1.0.0
    5. gunicorn==20.1.0
    6. itsdangerous==2.0.1
    7. Jinja2==3.0.3
    8. MarkupSafe==2.0.1
    9. numpy==1.21.4
    10. Werkzeug==2.0.2
    11. WTForms==3.0.0

## Вводные данные

- Матрица размера M x N (количество исполнителей и тем).
- Матрица графа времени исполнения задач.
- Оптимизация с помощью метода северо-западного угла или стандартным методом.

## Выходные данные

- Матрицы задаваемой размерности.
- Значение целевой функции.
- Информация о том, найден ли оптимальный путь и является ли он оптимальным.

## Как запустить программу

1. Перейдите в проект `transportation_problem_solver`.
2. Запустите функцию `main` в файле `run_server.py`.
3. В открывшемся терминале IDE перейдите по адресу `http://127.0.0.1:5000/`.
4. Протестируйте работоспособность программы.
5. Также можно посмотреть работоспособность на тестовом примере, для этого запустите функцию `main` в файле `example.py`, и в открывшемся браузере посмотрите страницу HTML.

## Полезные ссылки

1. [Статья на Хабре о решении транспортной задачи](https://habr.com/ru/articles/573224/)
2. [Шаблон решения на GitHub](https://github.com/electrobullet/transportation_problem_solver/tree/master/server)
3. [Кластерный метод решения транспортной задачи](https://habr.com/ru/articles/509656/)
4. [Поиск по Хабру по теме линейного программирования](https://habr.com/ru/search/?target_type=posts&order=relevance&q=[%D0%BB%D0%B8%D0%BD%D0%B5%D0%B9%D0%BD%D0%BE%D0%B5+%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5])
5. [Список программного обеспечения для оптимизации](https://en.wikipedia.org/wiki/List_of_optimization_software)

## Как его применить к нашему решению

Если дан граф или БД в виде файла excel, то можно по нему построить матрицу инцидентности (где исполнители и темы будут вершинами, а рёбра графа - временем, затрачиваемым на выполнение задачи), которую необходимо занести в программу вручную. Также, необходимо указать количество исполнителей и тем. После чего выбрать метод его оптимизации. Дальше будут получены и выведены результаты оптимизации.

## Что можно улучшить и доработать (TODO)

1. Поменять ввод данных - вместо ручного ввода матриц, сделать считываение файлов excel
2. Доработать веб-версию программы
3. Добавить параметры: время работы по оптимизированному критическому пути, коэффицент оперативности, коэффицент напряженности
