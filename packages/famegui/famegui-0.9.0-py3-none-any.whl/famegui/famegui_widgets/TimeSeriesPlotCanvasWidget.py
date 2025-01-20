from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


def extract_title_from_file_path(file_path: str) -> str:
    """Extract title string from given `file_path`"""
    result = Path(file_path).stem
    result = result.replace("_", " ")
    return result.title()


class TimeSeriesPlotCanvas(QObject):
    class PlotCanvas(FigureCanvas):
        def __init__(self, parent=None, width=5, height=6, dpi=80, file_path=None, title=None):
            fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)
            super().__init__(fig)
            self.setParent(parent)
            self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self.updateGeometry()
            self._file_path = file_path
            self._title = title

        def plot(self, x, y):
            self.ax.plot(x, y, 'r-')
            self.ax.set_title(self._title )
            self.ax.set_xlabel('Dates')
            y_label = extract_title_from_file_path(str(self._file_path))
            self.ax.set_ylabel(y_label)
            self.ax.grid(True)

            # Rotate x-axis labels for better readability
            self.ax.tick_params(axis='x', labelrotation=45)

            # Adjust tight layout to prevent overlapping
            plt.tight_layout()

            self.draw()

    def __init__(self, parent, file_path, title, start_date=None, end_date=None):
        super().__init__()

        self.canvas = self.PlotCanvas(parent, width=4, height=4, file_path=file_path, title=title)
        self.load_data_and_plot(file_path, start_date, end_date)

    def load_data_and_plot(self, file_path, start_date=None, end_date=None):
        # Load data
        data = pd.read_csv(file_path, delimiter=';')
        data.iloc[:, 0] = pd.to_datetime(data.iloc[:, 0], format='%Y-%m-%d_%H:%M:%S')

        # Filter by date range if provided
        if start_date:
            data = data[data.iloc[:, 0] >= pd.to_datetime(start_date)]
        if end_date:
            data = data[data.iloc[:, 0] <= pd.to_datetime(end_date)]

        x = data.iloc[:, 0]
        y = data.iloc[:, 1]

        # Plot data
        self.canvas.plot(x, y)
