import pandas as pd
import plotly.graph_objects as go
import genomenotebook as gn
import numpy as np
from typing import Optional, Tuple


class PeakCalling:
    """
    Class for analyzing significant coverage changes between two datasets.

    Attributes:
        data_1 (pd.DataFrame): The first dataset.
        data_2 (pd.DataFrame): The second dataset.
        window_size (int): The window size for calculating average coverage.
        threshold (float): The threshold for significant changes.
        changes (pd.DataFrame): Significant coverage changes.
    """

    def __init__(self, data_1: str, data_2: str, window_size: int, reads_count_1: int, 
                 reads_count_2: int, threshold: float = 0.6) -> None:
        """
        Initialize the PeakCalling class.

        Parameters:
            data_1 (str): Path to the first dataset.
            data_2 (str): Path to the second dataset.
            window_size (int): The window size for calculating average coverage.
            reads_count_1 (int): The number of reads in the first dataset.
            reads_count_2 (int): The number of reads in the second dataset.
            threshold (float): The threshold for significant changes (default is 0.6).
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
        Find significant coverage changes between the two datasets.

        Returns:
            pd.DataFrame: A table with significant coverage changes.
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
        Visualize the coverage with significant changes highlighted.
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
        Compare coverage changes with annotations in GFF format.

        Parameters:
            gff_annotation (str): Path to the GFF annotation file.
            bounds (tuple): The display bounds for the comparison graphs (default is (0, 120000)).
        """
        changes = self.find_significant_coverage_changes()

        left_bounds = changes['Start_Pos'].tolist()
        right_bounds = changes['End_Pos'].tolist()

        gff_path = gff_annotation

        # Create a GenomeBrowser object
        g = gn.GenomeBrowser(gff_path=gff_path, bounds=(0, 120000), search=False)

        # Add coverage graphs from each dataset
        track = g.add_track(height=350)
        track.line(data=self.data_1, pos="Position", y="Coverage", name=f"{self.dataset_name_1}", line_width=2)
        track.line(data=self.data_2, pos="Position", y="Coverage", name=f"{self.dataset_name_2}", line_color="green", line_width=2)

        # Highlight the regions of changes
        highlight_regions = pd.DataFrame({"left": left_bounds, "right": right_bounds, "color": "red"})
        track.highlight(data=highlight_regions, left="left", right='right', color="color")
        g.highlight(data=highlight_regions)

        # Show the result
        g.show()
        print(f'Green Line: {self.dataset_name_1}')
        print(f'Blue Line: {self.dataset_name_2}')
