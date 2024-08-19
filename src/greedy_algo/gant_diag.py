import matplotlib.pyplot as plt
import pandas as pd
from params_calc import calculate_params

early_start = 'Ранний старт'
early_finish = 'Раннее окончание'
latest_start = 'Поздний старт'
latest_finish = 'Позднее окончание'


# после разговора с товарищем подполквником:
# * строим по подзадачам
# * фиолетовый - начало работ + длительность
# * зеленый - фиолет + запас
# Загрузка пути к файлу


def build_gant(df, title, filepath_to_save):
    calculated_df, crit_path, crit_path_length = calculate_params(df)
    calculated_df = pd.merge(df, calculated_df, on='№ работы')
    # Создание диаграммы Ганта
    fig, ax = plt.subplots(figsize=(24, df.shape[0] / 2))

    # Рисование бара для каждой главной работы
    workers_labels = []
    for _, row in calculated_df.iterrows():
        row_y, row_width, row_x = row['№ работы'], row[early_finish] - row[early_start], row[early_start]
        color = 'red' if row['№ работы'] in crit_path else 'slateblue'

        ax.barh(row_y, row_width, left=row_x, align='center',
                color=color, label=row['Исполнитель'])

        workers_labels.append(row['Исполнитель'])

    for bar, text in zip(ax.patches, workers_labels):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_y() + bar.get_height() / 2, text, ha='center', va='center',
                fontsize=15)

    for _, row in calculated_df.iterrows():
        row_y, row_width, row_x = row['№ работы'], row[latest_finish] - row[early_finish], row[early_finish]
        if row_width != 0:
            ax.barh(row_y, row_width, left=row_x, color='yellowgreen', label=row['Исполнитель'])

    # Настройка осей и подписей
    ax.set_xlabel('Время (мин)')
    ax.set_ylabel('Главные работы')
    ax.set_title(title)
    # ax.legend()
    fig.savefig(f'{filepath_to_save}\\{title}.svg', dpi=300)
    # Отображение диаграммы
    # plt.show()
