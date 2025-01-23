import logging
import pandas as pd
from tqdm.autonotebook import tqdm
from scipy.interpolate import interp1d
from typing import Optional, List, Union
from utilsforecast.preprocessing import fill_gaps

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataFiller:
    """
    A class for filling missing data and performing interpolation on grouped DataFrame data.

    **Example Usage:**
    ```python
    filler = DataFiller(
        data=df,
        id='unique_id',
        date='ds',
        value=['sales', 'check_qnty'],
        freq='D',
        kind='linear',
        fill_value='extrapolate',
        verbose=True
    )
    filled_df = filler.fill_data()
    ```

    Args:
        data (pd.DataFrame): The input DataFrame to process.
        id (str, optional): Name of the identifier column. Defaults to 'unique_id'.
        date (str, optional): Name of the datetime column. Defaults to 'ds'.
        value (List[str], optional): List of columns to fill and interpolate. Defaults to ['sales', 'check_qnty'].
        freq (str, optional): Frequency for filling gaps (default is 'D' for daily). Defaults to 'D'.
        kind (str, optional): Type of interpolation (default is 'linear'). Defaults to 'linear'.
        fill_value (Union[str, float, None], optional): Fill value for interpolation outside data bounds. Defaults to 'extrapolate'.
        verbose (bool, optional): If True, displays a progress bar. Defaults to True.
        **fill_gaps_kwargs: Additional keyword arguments for the `fill_gaps` function.

    Attributes:
        data (pd.DataFrame): The input DataFrame.
        id_col (str): Identifier column name.
        date_col (str): Datetime column name.
        value_cols (List[str]): Columns to fill and interpolate.
        freq (str): Frequency for filling gaps.
        kind (str): Type of interpolation.
        fill_value (Union[str, float, None]): Fill value for interpolation outside data bounds.
        verbose (bool): Flag to display progress bar.
        fill_gaps_kwargs (dict): Additional keyword arguments for `fill_gaps`.
    """

    def __init__(
        self,
        data: pd.DataFrame,
        id: str = 'unique_id',
        date: str = 'ds',
        value: Optional[List[str]] = None,
        freq: str = 'D',
        kind: str = 'linear',
        fill_value: Union[str, float, None] = 'extrapolate',
        verbose: bool = True,
        **fill_gaps_kwargs
    ) -> None:
        self.data = data.copy()
        self.id_col = id
        self.date_col = date
        self.value_cols = value if value is not None else ['sales', 'check_qnty']
        self.freq = freq
        self.kind = kind
        self.fill_value = fill_value
        self.verbose = verbose
        self.fill_gaps_kwargs = fill_gaps_kwargs

        self._validate_input()

    def _validate_input(self) -> None:
        """Validates the input DataFrame and required columns."""
        if not isinstance(self.data, pd.DataFrame):
            raise TypeError("`data` must be a pandas DataFrame.")

        required_columns = [self.id_col, self.date_col] + self.value_cols
        missing_columns = [col for col in required_columns if col not in self.data.columns]
        if missing_columns:
            raise ValueError(f"The input DataFrame is missing required columns: {missing_columns}")

    def fill_data(
        self,
        start: str = 'per_serie',
        end: str = 'global'
    ) -> pd.DataFrame:
        """
        Fills missing values and performs interpolation on the data.

        Args:
            start (str, optional): Parameter for the `fill_gaps` function. Defaults to 'per_serie'.
            end (str, optional): Parameter for the `fill_gaps` function. Defaults to 'global'.

        Returns:
            pd.DataFrame: The filled and interpolated DataFrame.
        """
        # Internal renaming of columns for consistency
        df = self.data.rename(columns={
            self.id_col: 'unique_id',
            self.date_col: 'ds'
        }).copy()

        # Initialize an empty list to collect filled groups
        filled_groups = []

        # Group data by 'unique_id'
        groups = df.groupby('unique_id')
        total_groups = len(groups)

        # Initialize progress bar if verbose is True
        if self.verbose:
            groups = tqdm(groups, total=total_groups, desc='Filling Data:')

        for unique_id, group in groups:
            group = group[['unique_id', 'ds'] + self.value_cols].copy()

            # Ensure 'ds' is datetime
            if not pd.api.types.is_datetime64_any_dtype(group['ds']):
                try:
                    group['ds'] = pd.to_datetime(group['ds'])
                except Exception as e:
                    logger.error(f"Error converting 'ds' to datetime in group '{unique_id}': {e}")
                    continue

            # Sort by datetime
            group.sort_values('ds', inplace=True)

            # Check if value columns are numeric and warn if not
            numeric_cols = []
            for col in self.value_cols:
                if pd.api.types.is_numeric_dtype(group[col]):
                    numeric_cols.append(col)
                else:
                    logger.warning(
                        f"Column '{col}' is not numeric and will be skipped for interpolation in group '{unique_id}'."
                    )

            if not numeric_cols:
                logger.warning(f"No numeric columns to interpolate in group '{unique_id}'. Skipping.")
                filled_groups.append(group)
                continue

            # Fill gaps using the fill_gaps function
            try:
                filled_group = fill_gaps(
                    group,
                    freq=self.freq,
                    start=start,
                    end=end,
                    id_col='unique_id',
                    time_col='ds',
                    **self.fill_gaps_kwargs
                )
            except Exception as e:
                logger.error(f"Error filling gaps for group '{unique_id}': {e}")
                filled_groups.append(group)
                continue

            # Perform interpolation on specified columns
            for col in numeric_cols:
                filled_group = self._interpolate_column(filled_group, col, unique_id)

            filled_groups.append(filled_group)

        # Concatenate all filled groups
        filled_data = pd.concat(filled_groups, ignore_index=True)

        # Rename columns back to original names
        filled_data.rename(columns={
            'unique_id': self.id_col,
            'ds': self.date_col
        }, inplace=True)

        # Reorder columns for output
        ordered_columns = [self.id_col, self.date_col] + self.value_cols
        filled_data = filled_data.reindex(columns=ordered_columns)

        return filled_data

    def _interpolate_column(
        self,
        group: pd.DataFrame,
        column: str,
        unique_id: Union[int, str]
    ) -> pd.DataFrame:
        """
        Interpolates missing values in a specific column of a group.

        Args:
            group (pd.DataFrame): The group DataFrame.
            column (str): The column to interpolate.
            unique_id (Union[int, str]): The unique identifier of the group.

        Returns:
            pd.DataFrame: The group DataFrame with interpolated values.
        """
        nan_indices = group[group[column].isna()].index
        non_nan = group[group[column].notna()]

        if len(non_nan) < 2:
            logger.warning(
                f"Not enough data points to interpolate column '{column}' in group '{unique_id}'."
            )
            return group

        try:
            # Convert datetime to integer (seconds since epoch) for interpolation
            x = non_nan['ds'].astype('int64') // 10**9
            y = non_nan[column].astype(float)
            interp_func = interp1d(
                x,
                y,
                kind=self.kind,
                fill_value=self.fill_value,
                bounds_error=False
            )

            # Convert nan_indices 'ds' to integer format
            x_new = group.loc[nan_indices, 'ds'].astype('int64') // 10**9
            filled_values = interp_func(x_new)

            # Assign interpolated values
            group.loc[nan_indices, column] = filled_values
        except Exception as e:
            logger.error(f"Error interpolating column '{column}' for group '{unique_id}': {e}")

        return group

    def __repr__(self) -> str:
        return f"DataFiller(id_col='{self.id_col}', date_col='{self.date_col}', value_cols={self.value_cols})"
