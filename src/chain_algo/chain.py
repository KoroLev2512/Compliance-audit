import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

N = 6
M = 9

V = {
    11:[0.035785097,   0.005908865,	0.006997008,	0.015952846,	0.039496238,	0.013181947,	8.90983E-05,	0.036407781,	0.0714702],
    57:[0.027260918,	0.020665346,	0.003269431,	0.008212968,	0.070361251,	0.015478999,	0.000730106,	0.016262221,	0.042548078],
    71:[0.044895105,	0.007651944,	0.021126886,	0.016926649,	0.142113763,	0.006538688,	0.000316496,	0.038656269,	0.023802077],
    121:[0.154102168,	0.019021657,	0.105804876,	0.00141518,	    0.133891915,	0.042078225,	0.005449941,	0.121265509,	0.259952718],
    125:[0.044548624,	0.024189201,	0.006570725,	0.006717459,	0.25747662,	    0.038673947,	0.003414497,	0.039284976,	0.091346571],
    148:[0.073342414,	0.045818569,	0.097412974,	0.032516724,	0.249764899,	0.012914872,	0.002959509,	0.137712934,	0.304094137]
}

def optimize() -> pd.DataFrame:
    # Load data from Excel
    db1 = 'E:\\Users\\User3\\БД1.xlsx'
    db2 = 'E:\\Users\\User3\\БД2.xlsx'

    graph = __graph(db1)
    workers = __workers(db2)

    graph = __calculate_es_ef(graph)

    # print(graph.head(20))
    # print(workers.head(20))
    # traverse(graph, workers['Эксперт'].count())
    traverse(graph, workers)

    # Сохранение датафрейма в файл Excel
    graph_filename = 'graph.xlsx'
    graph.to_excel(graph_filename, index=False)
    workers_filename = 'workers.xlsx'
    workers.to_excel(workers_filename, index=False)

    print(f"Датафрейм сохранен в файлы: {graph_filename, workers_filename}")

    return

def traverse(graph: pd.DataFrame, workers: pd.DataFrame):
    # make topics
    graph['topic'] = graph['№ работы'].apply(lambda x: x.split('.')[0])
    topics = graph.groupby('topic').agg({'Длительность работы, мин': 'sum'}).reset_index()
    topics['topic'] = 'Тема ' + topics['topic']
    # topics_copy = topics.copy()
    # exclude last theme as common task
    
    # make top of workers by operative coeff
    top_workers = pd.DataFrame()
    top_coeff = pd.DataFrame()
    for theme in workers.columns[1:]:
        top = workers[['Эксперт', theme]].sort_values(by=theme, ascending=False).reset_index(drop=True)
        top_workers[theme] = top['Эксперт']
        top_coeff[theme] = top[theme]
    
    print(top_workers)
    # top_workers.to_csv('top_workers')
    # print(top_coeff)
    # top_coeff.to_csv('top_coeff')
    
    
    topics = topics.sort_values(by='Длительность работы, мин', ascending=False).reset_index(drop=True)
    # print(topics)

    works = pd.DataFrame()
    works['worker'] = workers['Эксперт']
    works['path'] = ''
    works['duration'] = 0
    # works['optimized_duration'] = 0

    
    # print(topics)
    
    for theme in top_workers.columns:
        worker = top_workers[theme][0]
        duration: int = topics.loc[topics['topic'] == theme, 'Длительность работы, мин'].item()

        # print(f'theme: {theme}, worker: {worker}, duration: {duration}')

        works.loc[works['worker'] == worker, 'path'] +=  '.' + theme.split(' ')[1]
        works.loc[works['worker'] == worker, 'duration'] += duration
        # works['optimized_duration'] += new_duration(worker, theme, duration)

        
        # print(works)
        
    print('#1 optimization - top operative coeff')
    print(works)
    # it should take the max duration worker
    # then parse his path and try to reassign job to another worker by top op coeff if worker1['newduration'] > worker2['newduration'],
    # else continue to next worker and if worker == -1 continue to next job
    # take next max duration worker and if it equals last one, break
    
    # tasks should be reassigned by ascending order
    last_worker = 0
    while True:
        # duration_max_id = works['optimized_duration'].idxmax()

        duration_max_id = works['duration'].idxmax()
        worker_row = works.loc[duration_max_id]
        if last_worker == worker_row['worker']:
            break
        last_worker = worker_row['worker']
        
        jobs = worker_row['path'].split('.')[1:]
        value_dict = dict(zip(topics['topic'], topics['Длительность работы, мин']))
        sorted_jobs = sorted(jobs, key=lambda x: value_dict['Тема ' + x])
        # print(jobs)
        # print(value_dict)
        # print(sorted_jobs)

        # print(topics)
        for topic in sorted_jobs:
            # if topic == '':
            #     print('hi')
            #     continue
            # print(topic)
                        
            duration_theme = topics.loc[topics['topic'] == 'Тема ' + topic, 'Длительность работы, мин'].item()
            # print(f'duration_theme: {duration_theme}')
            # print(worker_row)
            # duration_worker = worker_row['duration'].item()
            # print(f'duration_worker: {duration_worker}')
            
            index = top_workers[top_workers['Тема ' + topic] == worker_row['worker']].index[0]
            next_worker = -1
            while True:
                if index + 1 >= len(top_workers['Тема ' + topic]):
                    next_worker = -2
                    break
                next_worker = top_workers.iloc[index + 1]['Тема ' + topic]

                # print(f'next_worker: {next_worker}')
                
                # here you should try next worker by op coef and if it len() == index continue to next job
                # if works[works['worker'] == next_worker]['optimized_duration'].item() + new_duration(next_worker, topic, duration_theme) >= works[works['worker'] == worker_row['worker'].item()]['optimized_duration'].item():

                if works[works['worker'] == next_worker]['duration'].item() + duration_theme >= works[works['worker'] == worker_row['worker'].item()]['duration'].item():
                    index += 1
                    continue
                    
                works.loc[works['worker'] == worker_row['worker'], 'duration'] -= duration_theme
                # works.loc[works['worker'] == worker_row['worker'], 'optimized_duration'] -= new_duration(worker_row['worker'], topic, duration_theme)
                works.loc[works['worker'] == worker_row['worker'], 'path'] = works.loc[works['worker'] == worker_row['worker'], 'path'].item().replace(f'.{topic}', '')
                
                works.loc[works['worker'] == next_worker, 'duration'] += duration_theme
                # works.loc[works['worker'] == next_worker['worker'], 'optimized_duration'] += new_duration(next_worker['worker'], topic, duration_theme)
                works.loc[works['worker'] == next_worker, 'path'] = works.loc[works['worker'] == next_worker, 'path'].item() + f'.{topic}'

                
                worker_row['duration'] =  works.loc[duration_max_id, 'duration']
                # worker_row['optimized_duration'] =  works.loc[duration_max_id, 'optimized_duration']

                
                break
                

            # if next_worker == -1:
            #     print('next_worker not found')
            #     # return
            # if next_worker == -2:
            #     print('couldnt optimize topic among other workers')

    print('#2 optimization - reduce critical path in relation to the next top coeff')
    print(works)
    
    
    # take worker with critical path
    # while True:
    #     duration_max_id = works['duration'].idxmax()
    #     worker_row = works.loc[duration_max_id]
    #     if last_worker == worker_row['worker']:
    #         break
    #     last_worker = worker_row['worker']
    
    # print(graph)
    topics_jobs = graph[['№ работы', 'Длительность работы, мин', 'topic']]
    # print(topics_jobs)
    # expand topic into tasks
    # for index, worker_row in works.iterrows():
    #     path = ''
    #     for topic in worker_row['path'].split('.'):
    #         if topic == '' or topic == ' ':
     
    #             continue
            
    #         for job in graph[graph['topic'] == topic]['№ работы'].items():
    #             # print(job[1])
    #             path += f'`-{job[1]}'
    #             # return
    #         path += '`->'
    #     works.loc[index, 'path'] = path
        
    # print(works)
    # works.to_excel('works.xlsx')
        
    # get the critical path
    # try to assign workers to critical path (at least after em's path done) and calculate new duration (with shift)
    # get new critical path and optimize
    # if critical path is the same, optimization is done
    # while True:
    #     max_path = works['duration'].idxmax()
    #     min_path = works['duration'].idxmin()
    
    critical_path = works['duration'].idxmax()
    
    # get maximum critical path
    # get topics by that path
    # sort(?) jobs and get ascending(?) job 
    # get next worker and calculate new duration time
    
    
    # min_time_unit = works['duration']
    timeline = [0] * critical_path
    
    # optimize critical path by every opportunity
    # if new critical path is found, change target and optimize new one
    
    # assign finish topic (report) to every worker
    
    # exclude chairman and his tasks from common dataframe and count his fixed path (theme 1, 9, 10.1)
    # this man doesn't help others or expect to be helped.
        
    # print(topics_jobs)
    # print(topics_jobs.groupby('topic')['Длительность работы, мин'].apply(list).to_dict())
    # return
       

    # tasks_by_topic = topics_jobs.groupby('topic')['Длительность работы, мин'].apply(list).to_dict()
    # print(tasks_by_topic)

    # print(top_workers[top_workers.columns[0]][0])
    # for worker in top_workers[]
    # print(path)
        
    return

def new_duration(worker, theme, duration) -> int:
    # N - worker
    # M - themes
    # v - coeff op
    # duration - planned duration
    
    # get theme and shift it from 1 to 0
    theme = int(theme.split(' ')[1]) - 1
    return (1-1/(N*M)* V[worker][theme])*duration
    
def __workers(path: str) -> pd.DataFrame:
    df = pd.read_excel(path, sheet_name=1)

    return df


def __graph(path: str) -> pd.DataFrame:
    df = pd.read_excel(path,
                       dtype={
                           '№ работы': str,
                           'Предшествующая работа': str,
                           'Следующая работа': str
                       })
    df['ES'] = 0
    df['EF'] = 0

    return df


# Функция для расчета ES и EF (Ранний старт, Ранний финиш)
# Совпадает с LS и LF, если не задана временная граница
def __calculate_es_ef(df) -> pd.DataFrame:
    for i in range(len(df)):
        if df.at[i, 'Предшествующая работа'] == '0':
            df.at[i, 'ES'] = 0
        else:
            predecessor_ef = df[df['№ работы'] == df.at[i, 'Предшествующая работа']]['EF'].values[0]
            df.at[i, 'ES'] = predecessor_ef
        df.at[i, 'EF'] = df.at[i, 'ES'] + df.at[i, 'Длительность работы, мин']
    return df


optimize()
