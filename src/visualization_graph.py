import random

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from tkinter import filedialog
import os
import logging

from pyvis.network import Network

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Кол-во задач, которые могут отображаться на одной линии
nodes_number_on_line = 8


# Функция для получения основной задачи
def get_main_task(task):
    if task in ["Начало", "Окончание"]:
        return task
    if '.' in task:
        return task.split('.')[0]
    return task


def calculate_grid(df, distance=15, y_spacing=25, offset=60):
    df['Главная работа'] = df['№ работы'].apply(lambda a: a.split('.')[0])
    df['Исполнитель'] = df['Исполнитель'].apply(lambda a: str(a))
    # считаем кол-во уникальных исполнителей для таски
    groups = dict(list(df.groupby(['Главная работа', 'Исполнитель'])))
    # кол-во линий, которые необходимо выделить для темы
    lines_for_theme = {}
    # кол-во линий, которые необходимо выделить для задач исполнителя
    lines_for_theme_worker = {}
    for group in groups:
        group_content = groups[group]
        # кол-во линий, на которых можно разместить ноды текущего исполнителей
        lines_for_task = group_content.shape[0] // nodes_number_on_line \
            if group_content.shape[0] >= nodes_number_on_line else 1
        if len(str(group[1]).split(',')) <= 1:
            if group[0] in lines_for_theme:
                lines_for_theme[group[0]] = lines_for_theme[group[0]] + lines_for_task
            else:
                lines_for_theme[group[0]] = lines_for_task
            lines_for_theme_worker[(group[0], str(group[1]))] = lines_for_task
    tasks_y = {}

    main_tasks = sorted(lines_for_theme, key=int)
    for i, task in enumerate(main_tasks):
        next_tasks = main_tasks[i + 1::]
        summ = lines_for_theme[task]
        for next_task_number in next_tasks:
            summ += lines_for_theme[next_task_number]
        tasks_y[task] = summ
    pos = {}
    # расположение основных задач
    first_task_y = None
    last_task_y = 0
    for i, task in enumerate(sorted(lines_for_theme, key=int)):
        y_pos = (tasks_y[task] - (lines_for_theme[task]) // 2) * (y_spacing + offset)
        pos[task] = (-distance, y_pos)
        if first_task_y is None:
            first_task_y = y_pos
        last_task_y = y_pos

    # распеределние самих подзадач

    lines_content = {}
    # tasks_y[1] хранит в себе сумму всех линий первой и последующих тем
    for line_number in range(tasks_y['1'] + 20):
        lines_content[line_number] = []

    # оперделяем какие задачи будут на каждой линии
    current_line = 0
    starter_works_for_task = []
    for task_number, worker in sorted(list(lines_for_theme_worker.keys()), key=lambda x: int(x[0])):
        if len(lines_content[current_line]) > nodes_number_on_line:
            current_line += 1
        group_tasks = groups[(task_number, worker)]

        # получаем работы текущего исполнителя в нужном порядке
        starting_works = group_tasks[group_tasks['Предшествующая работа'] == task_number]['№ работы'].tolist()
        starting_works += group_tasks[(~group_tasks['Предшествующая работа'].isin(group_tasks['№ работы']))
                                      & (group_tasks['№ работы'] != task_number)]['№ работы'].tolist()

        starter_works_for_task += starting_works
        ordered_works = []

        for work in starting_works:
            add_jobs(work, task_number, ordered_works, group_tasks)
        print(ordered_works)
        processed_work = []
        for work in ordered_works:
            if work not in processed_work:
                lines_content[current_line].append(work)
                processed_work.append(work)
            if len(lines_content[current_line]) > nodes_number_on_line:
                current_line += 1
        if len(lines_content[current_line]) != 0:
            current_line += 1

    current_main_task = -1
    for line_number in lines_content:
        if len(lines_content[line_number]) == 0:
            continue
        if current_main_task != get_main_task(lines_content[line_number][0]):
            current_main_task = get_main_task(lines_content[line_number][0])
            local_line_count = 0
            lines = lines_for_theme[current_main_task]
            task_node_y = pos[current_main_task]
        for j, work_number in enumerate(lines_content[line_number]):
            if work_number not in main_tasks:
                pos[work_number] = (
                    (j + 2) * distance, task_node_y[1] + (lines // 2 - local_line_count) * (y_spacing + offset / 2))
        local_line_count += 1

    return pos, first_task_y, last_task_y, lines_for_theme_worker, starter_works_for_task


def add_jobs(job, task_number, ordered_works, group_tasks):
    ordered_works.append(job)
    next_work = group_tasks[group_tasks['Предшествующая работа'] == job]['№ работы']
    if not next_work.empty:
        add_jobs(next_work.values[0], task_number, ordered_works, group_tasks)


# Функция для генерации позиций вершин
def generate_positions(df, distance=15):
    pos, first_task_y, last_task_y, lines_for_theme_worker, start_works = calculate_grid(df)

    # Расположение начальной и конечной вершин
    pos["Начало"] = (-distance * 2, (first_task_y + last_task_y + 1) // 2)

    # Расположение "Окончание" в зависимости от максимального количества троек подзадач
    pos["Окончание"] = (distance * (nodes_number_on_line + 5), (first_task_y + last_task_y + 1) // 2)

    return pos, start_works


def generate_svg_graph(df, filepath_to_save):
    if df is not None:
        # Преобразование столбцов "№ работы" и "Предшествующая работа" в строки
        df['№ работы'] = df['№ работы'].astype(str)
        df['Предшествующая работа'] = df['Предшествующая работа'].astype(str)

        # Удаление дубликатов
        df = df.drop_duplicates()

        # Выбор только необходимых столбцов
        df = df[['№ работы', 'Предшествующая работа', 'Исполнитель', 'Следующая работа']]

        # Генерация позиций вершин
        last_task = max(list(map(int, df['№ работы'].apply(lambda x: get_main_task(x)).unique())))
        df['Главная задача'] = df['№ работы'].apply(lambda x: get_main_task(x))
        df = df.drop(df[df['Главная задача'] == str(last_task)].index)
        pos, starter_works = generate_positions(df)

        # Создание графа
        G = nx.DiGraph()
        edge_labels = {}
        for starter in starter_works:
            G.add_edge(get_main_task(starter), starter)

        # Добавление вершин и ребер
        for i, row in df.iterrows():
            current_task = row['№ работы']
            next_task = row['Следующая работа']
            if int(get_main_task(current_task)) == last_task:
                continue
            G.add_node(current_task, исполнитель=row['Исполнитель'])
            if int(get_main_task(next_task)) >= last_task:
                G.add_edge(current_task, 'Окончание')
            elif get_main_task(current_task) == get_main_task(next_task):
                G.add_edge(current_task, next_task)
            else:
                G.add_edge(current_task, get_main_task(next_task))
                edge_labels[(current_task, get_main_task(next_task))] = row['Исполнитель']

        # Добавление начальной и конечной вершин
        G.add_node("Начало", исполнитель="Начало")
        G.add_node("Окончание", исполнитель="Окончание")

        # Связывание начальной вершины с задачами, у которых нет предшествующих работ
        for node in G.nodes():
            if G.in_degree(node) == 0 and node != "Начало":
                G.add_edge("Начало", node)

        # Убедитесь, что все узлы имеют атрибут "исполнитель"
        for node in G.nodes():
            if 'исполнитель' not in G.nodes[node]:
                G.nodes[node]['исполнитель'] = 'Unknown'

        # Удаление лишнего ребра из "Начало" в "Окончание"
        if G.has_edge("Начало", "Окончание"):
            G.remove_edge("Начало", "Окончание")

        # Словарь для хранения количества исполнителей для каждой основной задачи
        task_performers = {}
        for node in G.nodes():
            main_task = get_main_task(node)
            if main_task not in task_performers:
                task_performers[main_task] = set()
            task_performers[main_task].add(G.nodes[node]['исполнитель'])

        # раскраска нод
        workers_colors = pd.DataFrame({'Исполнитель': df['Исполнитель'].unique()})
        workers_colors['rgb'] = 'lightblue'

        for i, row in workers_colors.iterrows():
            r = random.randint(54, 255)
            g = random.randint(182, 255)
            b = random.randint(18, 255)
            workers_colors.loc[workers_colors['Исполнитель'] == row['Исполнитель'], 'rgb'] = f'#{r:02X}{g:02X}{b:02X}'

        node_colors = []
        for node in G.nodes():
            if '.' in node:
                worker = G.nodes[node]['исполнитель']
                color = workers_colors[workers_colors['Исполнитель'] == worker]['rgb'].values
                if color.shape[0] > 0:
                    node_colors.append(color[0])
                else:
                    node_colors.append('lightblue')
            else:
                node_colors.append('lightblue')

        # Отображение графа
        fig, ax = plt.subplots(figsize=(25, 25))  # Увеличенный размер фигуры
        nx.draw(G, pos, with_labels=True, node_size=200, node_color=node_colors, font_size=4, font_weight='bold',
                arrows=True, ax=ax)

        # Добавление исполнителей к ребрам
        edge_labels = {}
        for u, v in G.edges():
            if (G.nodes[v]['исполнитель'] == 'Unknown') and \
                    (get_main_task(u) != get_main_task(v)):
                edge_labels[(u, v)] = G.nodes[u]['исполнитель']
            elif u != "Начало" and v != "Окончание":
                edge_labels[(u, v)] = G.nodes[v]['исполнитель']
            elif u == "Начало":
                edge_labels[(u, v)] = G.nodes[v]['исполнитель']
            elif v == "Окончание":
                edge_labels[(u, v)] = G.nodes[u]['исполнитель']

        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=3, ax=ax)
        plt.title("Сетевой граф задач", fontsize=10)

        # Сохранение графика в файл с фактическими размерами
        # output_filename = os.path.splitext(os.path.basename(filepath_bd_1))[0] + '_graph.svg'
        plt.savefig(f'{filepath_to_save}\\Граф оптимизация.svg', dpi=300, bbox_inches='tight')
        logging.info("График сохранен в файл: %s", f'{filepath_to_save}\\Граф оптимизация.svg')

        return G


if __name__ == "__main__":
    # Загрузка пути к файлу
    filepath_bd_1 = filedialog.askopenfilename()
    if not filepath_bd_1:
        logging.error("Файл не выбран")
    else:
        logging.info("Открыт файл БД 1: %s", filepath_bd_1)

        try:
            # Загрузка данных из Excel
            df = pd.read_excel(filepath_bd_1)
        except Exception as e:
            logging.error("Ошибка при чтении файла Excel: %s", e)
            df = None
        output_folder_path = os.path.dirname(os.path.realpath(filepath_bd_1))
        G = generate_svg_graph(df, output_folder_path)
