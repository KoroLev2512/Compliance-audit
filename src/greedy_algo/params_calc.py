import pandas as pd
import networkx as nx
from pyvis.network import Network


# def visualize_graph(workers, themes_len):
#     # Создание графа
#     G = nx.DiGraph()
#
#     pivots = []
#     for theme_index in range(1, themes_len + 1):
#         G.add_node(str(theme_index), group=str(theme_index))
#         for worker in workers:
#             worker_tasks_in_current_theme = list(filter(lambda a: a.theme == theme_index, worker.history))
#             if len(worker_tasks_in_current_theme) > 0:
#                 G.add_node(worker_tasks_in_current_theme[0].name, group=str(theme_index))
#                 G.add_edge(str(theme_index), worker_tasks_in_current_theme[0].name,
#                            label=f'{worker.name}, {worker_tasks_in_current_theme[0].duration}')
#
#                 for i in range(1, len(worker_tasks_in_current_theme)):
#                     G.add_node(worker_tasks_in_current_theme[i].name, group=str(theme_index))
#                     G.add_edge(worker_tasks_in_current_theme[i - 1].name, worker_tasks_in_current_theme[i].name,
#                                label=f'{worker.name}, {worker_tasks_in_current_theme[i].duration}')
#
#                 last_task_worker_in_theme = worker_tasks_in_current_theme[-1]
#                 if last_task_worker_in_theme.theme < themes_len:
#                     next_task_after_last_task_worker_in_theme = worker.history[worker.history.index(last_task_worker_in_theme) + 1]
#                     pivots.append((last_task_worker_in_theme, next_task_after_last_task_worker_in_theme.theme, worker.name))
#
#     for task, theme, worker_name in pivots:
#         G.add_edge(task.name, theme, label=f'{worker_name}, {task.duration}')
#
#     # Создание pyvis сети
#     nt = Network(notebook=True, height='900px', directed=True)
#
#     # Преобразование networkx графа в pyvis граф
#     nt.from_nx(G)
#
#     nt.set_options("""
#     {
#         "layout": {
#             "hierarchical": {
#                 "enabled": true,
#                 "direction": "UD",
#                 "sortMethod": "directed"
#             }
#         },
#         "physics": {
#             "enabled": false
#         }
#     }
#     """)
#
#     # Отображение графа
#     nt.show('graph.html')


# расчитать параметры (ранний старт, ранний финиш...)
def calculate_params(df):
    # Создание графа
    G = nx.DiGraph()

    # Добавление узлов и рёбер
    for _, row in df.iterrows():
        node = row['№ работы']
        duration = row['Длительность работы, мин']
        performer = row['Исполнитель']
        group = node.split('.')[0]
        G.add_node(node, duration=duration, group=group)

        if pd.notna(row['Предшествующая работа']):
            predecessor = row['Предшествующая работа']
            G.add_edge(predecessor, node, label=performer)

        if pd.notna(row['Следующая работа']):
            successor = row['Следующая работа']
            G.add_edge(node, successor, label=performer)

    # Расчёт ранних сроков
    es = {}
    ef = {}
    for node in nx.topological_sort(G):
        predecessors = list(G.predecessors(node))
        if predecessors:
            es[node] = max(ef[pred] for pred in predecessors)
        else:
            es[node] = 0

        ef[node] = es[node] + G.nodes[node].get('duration', 0)

    # Расчёт поздних сроков
    ls = {}
    lf = {}
    for node in reversed(list(nx.topological_sort(G))):
        successors = list(G.successors(node))
        if successors:
            lf[node] = min(ls[suc] for suc in successors)
        else:
            lf[node] = ef[node]

        ls[node] = lf[node] - G.nodes[node].get('duration', 0)

    # Расчёт резервов
    total_slack = {}
    free_slack = {}
    for node in G.nodes:
        total_slack[node] = ls[node] - es[node]
        free_slack[node] = min((ls[suc] - ef[node] for suc in G.successors(node)), default=total_slack[node])

    # Коэффициенты напряжённости
    intensity = {node: G.nodes[node].get('duration', 0) / total_slack[node] if total_slack[node] > 0 else float('inf')
                 for
                 node in
                 G.nodes}

    # Результаты
    results = {
        '№ работы': [],
        'Ранний старт': [],
        'Раннее окончание': [],
        'Поздний старт': [],
        'Позднее окончание': [],
        'Свободный резерв': [],
        'Полный резерв': [],
        'Коэффициент напряженности': []
    }

    for node in G.nodes:
        results['№ работы'].append(node)
        results['Ранний старт'].append(es[node])
        results['Раннее окончание'].append(ef[node])
        results['Поздний старт'].append(ls[node])
        results['Позднее окончание'].append(lf[node])
        results['Свободный резерв'].append(free_slack[node])
        results['Полный резерв'].append(total_slack[node])
        results['Коэффициент напряженности'].append(intensity[node])

    # Создание DataFrame для результатов
    params_df = pd.DataFrame(results)
    params_df = params_df.sort_values(by='Коэффициент напряженности')
    print(params_df.tail(50))

    # Нахождение критического пути
    critical_path_length = max(ef[node] for node in G.nodes)

    # Поиск критического пути
    def find_critical_path(graph, end_node):
        path = []
        node = end_node
        while node:
            path.append(node)
            predecessors = list(graph.predecessors(node))
            if predecessors:
                # Если несколько предшественников, берем тот, который также находится на критическом пути
                node = max(predecessors, key=lambda pred: ef[pred] if ef[pred] == es[node] else -1, default=None)
            else:
                node = None
        return list(reversed(path))

    # Критический путь должен заканчиваться на узлах, у которых время окончания равно критическому времени
    critical_path_nodes = []
    for node in G.nodes:
        if ef[node] == critical_path_length:
            critical_path_nodes = find_critical_path(G, node)
            break

    # Вывод времени критического пути
    print(f"Время критического пути: {critical_path_length} минут")

    # Вывод узлов критического пути
    print("Узлы критического пути:")
    print(critical_path_nodes)

    # Добавляем временную колонку с преобразованными значениями
    params_df['parsed'] = params_df['№ работы'].apply(lambda a: list(map(int, a.split('.'))))

    # Сортируем DataFrame по временной колонке
    params_df = params_df.sort_values(by='parsed')

    # Удаляем временную колонку
    params_df = params_df.drop(columns=['parsed'])

    return params_df, critical_path_nodes, critical_path_length
