import pandas as pd
import plotly.graph_objects as go
import genomenotebook as gn
import numpy as np
from typing import Optional, Tuple


class PeakCalling:
    """
    Класс для анализа значительных изменений покрытия между двумя наборами данных.

    Атрибуты:
        data_1 (pd.DataFrame): Первый набор данных.
        data_2 (pd.DataFrame): Второй набор данных.
        window_size (int): Размер окна для расчета среднего покрытия.
        threshold (float): Пороговое значение для значительных изменений.
        changes (pd.DataFrame): Значительные изменения покрытия.
    """

    def __init__(self, data_1: str, data_2: str, window_size: int, reads_count_1: int, 
                 reads_count_2: int, threshold: float = 0.6) -> None:
        """
        Инициализация класса PeakCalling.

        Параметры:
            data_1 (str): Путь к первому набору данных.
            data_2 (str): Путь ко второму набору данных.
            window_size (int): Размер окна для расчета среднего покрытия.
            reads_count_1 (int): Количество прочтений в первом наборе данных.
            reads_count_2 (int): Количество прочтений во втором наборе данных.
            threshold (float): Пороговое значение для значительных изменений (по умолчанию 0.6).
        """
        self.data_1 = pd.read_csv(data_1, sep='\t', header=None, names=['Sample', 'Position', 'Coverage'])
        self.data_2 = pd.read_csv(data_2, sep='\t', header=None, names=['Sample', 'Position', 'Coverage'])
        self.data_1['Coverage'] = self.data_1['Coverage'] / reads_count_1
        self.data_2['Coverage'] = self.data_2['Coverage'] / reads_count_2

        self.dataset_name_1 = data_1
        self.dataset_name_2 = data_2
        self.threshold = threshold
        self.window_size = window_size
        self.changes = pd.DataFrame()

    def find_significant_coverage_changes(self) -> pd.DataFrame:
        """
        Поиск значительных изменений покрытия между двумя наборами данных.

        Возвращает:
            pd.DataFrame: Таблица со значительными изменениями покрытия.
        """
        data_1 = self.data_1
        data_2 = self.data_2

        data_1['Window'] = (data_1['Position'] - 1) // self.window_size
        data_2['Window'] = (data_2['Position'] - 1) // self.window_size

        coverage_1 = data_1.groupby('Window').agg({'Coverage': 'mean', 'Position': ['min', 'max']}).reset_index()
        coverage_1.columns = ['Window', 'Avg_Coverage_1', 'Start_Pos', 'End_Pos']

        coverage_2 = data_2.groupby('Window').agg({'Coverage': 'mean', 'Position': ['min', 'max']}).reset_index()
        coverage_2.columns = ['Window', 'Avg_Coverage_2', 'Start_Pos_2', 'End_Pos_2']

        merged = pd.merge(coverage_1, coverage_2, on='Window')
        merged['Change'] = abs(merged['Avg_Coverage_1'] - merged['Avg_Coverage_2']) / merged[['Avg_Coverage_1', 'Avg_Coverage_2']].max(axis=1)

        significant_changes = merged[merged['Change'] > self.threshold]
        self.changes = significant_changes[['Window', 'Change', 'Start_Pos', 'End_Pos']]
        return self.changes

    def visualize_coverage(self) -> None:
        """
        Визуализация покрытия с выделением значительных изменений.
        """
        fig = go.Figure()

        fig.add_trace(go.Scatter(x=self.data_1['Position'], y=self.data_1['Coverage'], mode='lines',
                                 name=f'Coverage Set of "{self.dataset_name_1}"'))
        fig.add_trace(go.Scatter(x=self.data_2['Position'], y=self.data_2['Coverage'], mode='lines',
                                 name=f'Coverage Set of "{self.dataset_name_2}"'))

        for _, row in self.changes.iterrows():
            fig.add_vrect(x0=row['Start_Pos'], x1=row['End_Pos'], fillcolor="LightSalmon", opacity=0.5, line_width=0)

        fig.update_layout(title='Coverage Comparison with Significant Changes Highlighted',
                          xaxis_title='Position', yaxis_title='Coverage',
                          template='plotly_white')
        fig.show()

    def compare_coverage_changes_with_annotation(self, gff_annotation: str, bounds: tuple = (0, 120000)) -> None:
        """
        Сравнение изменений покрытия с аннотациями в формате GFF.

        Параметры:
            gff_annotation (str): Путь к файлу аннотаций GFF.
            bounds (tuple): Границы отображения графиков для сравнения с аннотацией (по умолчанию (0, 120000)).
        """
        changes = self.find_significant_coverage_changes()

        left_bounds = changes['Start_Pos'].tolist()
        right_bounds = changes['End_Pos'].tolist()

        gff_path = gff_annotation

        # Создаем объект GenomeBrowser
        g = gn.GenomeBrowser(gff_path=gff_path, bounds=(0, 120000), search=False)

        # Добавляем графики покрытий из каждого набора данных
        track = g.add_track(height=350)
        track.line(data=self.data_1, pos="Position", y="Coverage", name=f"{self.dataset_name_1}", line_width=2)
        track.line(data=self.data_2, pos="Position", y="Coverage", name=f"{self.dataset_name_2}", line_color="green", line_width=2)

        # Подсвечиваем область изменений 
        highlight_regions = pd.DataFrame({"left": left_bounds, "right": right_bounds, "color": "red"})
        track.highlight(data=highlight_regions, left="left", right='right', color="color")
        g.highlight(data=highlight_regions)

        # Показываем результат
        g.show()
        print(f'Green Line: {self.dataset_name_1}')
        print(f'Blue Line: {self.dataset_name_2}')
