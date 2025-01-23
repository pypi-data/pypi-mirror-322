import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from ipywidgets import interact, FloatSlider, IntSlider, widgets, HBox, VBox
from IPython.display import set_matplotlib_formats
set_matplotlib_formats('retina')

class Detector:
    """
    A class for detecting and visualizing outliers in time series data using interactive widgets.

    The `Detector` class is designed to work with time series data stored in a pandas DataFrame, allowing for the detection and visualization of outliers. It supports automatic detection of identifier, time, and numeric columns, and offers an interactive interface using ipywidgets to explore the data and adjust parameters like standard deviation and window size for outlier detection.

    Attributes:
        df (pd.DataFrame): The DataFrame containing the time series data, which may include identifier, time, and numeric columns.
        id_column (str): The detected identifier column name.
        time_column (str): The detected time column name.
        numeric_columns (list): A list of detected numeric column names in the DataFrame.

    Methods:
        __init__(df: pd.DataFrame):
            Initializes the Detector class, automatically handles missing identifier or datetime index, and detects the appropriate columns for analysis.

        _handle_missing_id_and_index():
            Handles cases where the identifier or time column is missing by creating defaults or resetting indices if necessary.

        _detect_columns():
            Automatically detects columns that contain date values, identifiers, and numeric data.

        interactive_outlier_visualization(series_id: int, column: str, std_dev: float, window: int, start_date, end_date):
            Creates an interactive visualization for analyzing a specific series with adjustable outlier detection parameters.

        run():
            Launches the interactive widget interface for exploring time series data with outlier detection.

    Usage:
        Detector(df)
        
        # This will automatically detect columns and launch an interactive interface.
        # Users can adjust parameters for outlier detection and interactively visualize the results.

    Example:
        # Assuming `df` is a pandas DataFrame containing columns: 'id', 'date', 'value'.
        Detector(df)
        
        # After initializing, the `run()` method is called automatically, which launches an interactive widget.
        # Users can explore different time series, adjust parameters for outlier detection, and visualize the results.

    """

    def __init__(self, df: pd.DataFrame):
        """
        Initialize the Detector class with the provided DataFrame.

        Args:
            df (pd.DataFrame): Input DataFrame containing time series data, with potential identifier and numerical columns.
        """
        if not isinstance(df, pd.DataFrame):
            raise TypeError("Input data must be a pandas DataFrame.")
        if df.empty:
            raise ValueError("The provided DataFrame is empty. Please provide a non-empty DataFrame.")
        
        self.df = df
        self.id_column = None
        self.time_column = None
        self.numeric_columns = []

        self._handle_missing_id_and_index()
        self._detect_columns()
        self.run()

    def _handle_missing_id_and_index(self) -> None:
        """
        Handle cases where ID is missing or time is in the index.
        - If the DataFrame index is a DatetimeIndex, reset it and rename to 'ds'.
        - If there is no ID column and only one time series, create a dummy ID column.
        """
        if isinstance(self.df.index, (pd.DatetimeIndex, pd.Timestamp)):  # Check if the index is datetime-based
            self.df = self.df.reset_index().rename(columns={'index': 'ds'})

        if 'id' not in self.df.columns and len(self.df.columns) > 1:
            self.df['id'] = 1

    def _detect_columns(self) -> None:
        """
        Automatically detect columns containing date, identifiers, and numerical values.
        - Assign the time column, ID column, and numeric columns based on data types and uniqueness.
        """
        # Detect the time column based on datetime type or name
        for column in self.df.columns:
            if pd.api.types.is_datetime64_any_dtype(self.df[column]) or column.lower() in ['date', 'datetime', 'timestamp']:
                self.time_column = column
                break

        if self.time_column is None:
            raise ValueError("Could not find a valid time column. Please make sure the DataFrame contains a column with datetime values.")

        # Detect ID column based on keyword "id" and ensure it's not mistaken for time
        for column in self.df.columns:
            if 'id' in column.lower() and column != self.time_column:
                self.id_column = column
                break

        if self.id_column is None:
            raise ValueError("Could not find a valid ID column. Please make sure the DataFrame contains a column named 'id' or similar.")

        # Detect numeric columns based on data type
        for column in self.df.columns:
            if pd.api.types.is_numeric_dtype(self.df[column]) and column not in [self.id_column, self.time_column]:
                self.numeric_columns.append(column)

        if len(self.numeric_columns) == 0:
            raise ValueError("Could not find any numeric columns. Please make sure the DataFrame contains numeric data for analysis.")

    def interactive_outlier_visualization(self, series_id: int, column: str, std_dev: float, window: int, start_date, end_date) -> None:
        """
        Create an interactive visualization to adjust outlier detection parameters and time range.

        Args:
            series_id (int): Identifier of the series to visualize.
            column (str): Column to visualize.
            std_dev (float): Standard deviation multiplier for outlier bounds.
            window (int): Window size for calculating the moving average and standard deviation.
            start_date (datetime): Start date for visualization.
            end_date (datetime): End date for visualization.
        """
        if series_id not in self.df[self.id_column].unique():
            raise ValueError(f"The provided series ID '{series_id}' is not valid. Please select a valid ID from the dropdown options.")
        if column not in self.numeric_columns:
            raise ValueError(f"The provided column '{column}' is not numeric or not available. Please select a valid column from the dropdown options.")

        series_data = self.df[self.df[self.id_column] == series_id].copy()
        series_data = series_data.sort_values(by=self.time_column)

        mask = (series_data[self.time_column] >= pd.to_datetime(start_date)) & \
               (series_data[self.time_column] <= pd.to_datetime(end_date))
        series_data = series_data[mask]

        if series_data.empty:
            raise ValueError("No data available for the selected date range. Please select a different date range.")

        series_data['moving_average'] = series_data[column].rolling(window=window, min_periods=1, center=True).mean()
        series_data['std_dev'] = series_data[column].rolling(window=window, min_periods=1, center=True).std()

        series_data['lower_bound'] = series_data['moving_average'] - std_dev * series_data['std_dev']
        series_data['upper_bound'] = series_data['moving_average'] + std_dev * series_data['std_dev']

        outliers = (series_data[column] < series_data['lower_bound']) | (series_data[column] > series_data['upper_bound'])

        plt.figure(figsize=(15, 5))
        plt.plot(series_data[self.time_column], series_data[column], color='black', label='Original Data', alpha=0.5)
        plt.scatter(series_data[self.time_column][outliers], series_data[column][outliers], color='red', label='Outliers', zorder=5)
        plt.plot(series_data[self.time_column], series_data['moving_average'], color='blue', label='Moving Average')
        plt.fill_between(series_data[self.time_column], series_data['lower_bound'], series_data['upper_bound'], color='blue', alpha=0.2, label=f'{std_dev} Std Dev Bounds')
        plt.xlabel('Date')
        plt.ylabel(column)
        plt.title(f'{self.id_column.capitalize()} {series_id} - {column}')
        plt.grid(True)
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
        plt.show()

    def __repr__(self) -> str:
        return 'shakhbanov.org'

    def run(self) -> None:
        """
        Launch an interactive interface for analyzing all identifiers and columns with time range control.
        """
        if self.time_column is None or self.id_column is None or len(self.numeric_columns) == 0:
            raise ValueError("The required columns were not properly detected. Please check the DataFrame and try again.")

        date_min = self.df[self.time_column].min().date()
        date_max = self.df[self.time_column].max().date()

        series_id_widget = widgets.Dropdown(options=self.df[self.id_column].unique(), description='ID:')
        column_widget = widgets.Dropdown(options=self.numeric_columns, description='Column:')
        std_dev_widget = FloatSlider(value=2.0, min=0.5, max=5.0, step=0.1, description='Std Dev')
        window_widget = IntSlider(value=30, min=5, max=365, step=1, description='Window')
        start_date_widget = widgets.DatePicker(value=date_min, description='Start Date')
        end_date_widget = widgets.DatePicker(value=date_max, description='End Date')

        ui = VBox([
            HBox([series_id_widget, std_dev_widget, start_date_widget]),
            HBox([column_widget, window_widget, end_date_widget])
        ])

        out = widgets.interactive_output(
            self.interactive_outlier_visualization,
            {
                'series_id': series_id_widget,
                'column': column_widget,
                'std_dev': std_dev_widget,
                'window': window_widget,
                'start_date': start_date_widget,
                'end_date': end_date_widget
            }
        )

        display(ui, out)
