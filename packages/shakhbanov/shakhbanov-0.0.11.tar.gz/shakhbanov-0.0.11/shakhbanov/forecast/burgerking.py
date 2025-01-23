import logging
import warnings
import requests

import pandas as pd
import numpy as np

from functools import reduce
from datetime import datetime
from xgboost import XGBRegressor
from tqdm.autonotebook import tqdm
from sklearn.linear_model import LinearRegression

warnings.filterwarnings("ignore")


class HybridModel:
    """Defines a hybrid model combining Linear Regression and XGBoost."""

    def __init__(self, base_model1, base_model2):
        """Initializes the HybridModel with two base models.

        Args:
            base_model1: The first base model (e.g., Linear Regression).
            base_model2: The second base model (e.g., XGBoost).
        """
        self.base_model1 = base_model1
        self.base_model2 = base_model2

    def fit(self, X, y):
        """Fits the two base models.

        The first model is fit on the original target values, and the
        second model is fit on the residuals from the first model.

        Args:
            X: Feature matrix (array-like or pd.DataFrame).
            y: Target values (array-like or pd.Series).
        """
        self.base_model1.fit(X, y)
        y_fit1 = self.base_model1.predict(X)
        residuals1 = y - y_fit1
        self.base_model2.fit(X, residuals1)

    def predict(self, X):
        """Predicts using both base models and sums the results.

        Args:
            X: Feature matrix (array-like or pd.DataFrame).

        Returns:
            A 1D array of predictions.
        """
        y_pred1 = self.base_model1.predict(X)
        y_pred2 = self.base_model2.predict(X)
        y_pred = y_pred1 + y_pred2
        return y_pred


class BurgerKing:
    """Class for forecasting using a hybrid approach (Linear + XGBoost).

    Attributes:
        data: The primary dataset as a pd.DataFrame.
        id: The identifier column name (e.g., restaurant ID).
        target: A list of target variables.
        h: Forecast horizon (number of days).
        params: Hyperparameters for XGBoost.
        tqdm: Whether to use a progress bar.
        verbose: Whether to enable logging.
    """

    def __init__(self,
                 data,
                 id='rest_id',
                 target=['sales', 'check_qnty'],
                 h=180,
                 params=None,
                 tqdm=True,
                 verbose=True):
        """Initializes the BurgerKing class for forecasting.

        Args:
            data: pd.DataFrame, the main dataset.
            id: str, the name of the identifier column.
            target: list, the list of target variables.
            h: int, the forecast horizon (in days).
            params: dict, hyperparameters for XGBoost.
            tqdm: bool, whether to display a progress bar.
            verbose: bool, whether to enable logging output.
        """
        self.verbose = verbose
        self.logger = logging.getLogger('BurgerKing')
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        if self.verbose:
            self.logger.setLevel(logging.INFO)
        else:
            self.logger.setLevel(logging.WARNING)

        self.data = data
        self.id = id
        self.target = target
        self.h = h
        self.params = params if params is not None else {}
        self.tqdm = tqdm

        self.logger.info("Loading holiday data...")
        self.calendar = self._load_holiday_data()
        self.logger.info("Holiday data loaded.")

        self.logger.info("Loading and preparing main data...")
        self.df = self._load_and_prepare_data()
        self.logger.info("Main data prepared.")

        self.logger.info("Creating features...")
        self.df = self._create_features()
        self.logger.info("Features created.")

        self.logger.info("Defining feature sets for models...")
        self.feature_cols_dict = self._define_feature_columns()
        self.logger.info("Feature sets defined.")

    def _load_holiday_data(self):
        """Loads and processes holiday data from a public source.

        Returns:
            A pd.DataFrame with a date range and holiday flags.
        """
        url = "https://raw.githubusercontent.com/d10xa/holidays-calendar/master/json/calendar.json"
        response = requests.get(url)
        response.raise_for_status()
        json_data = response.json()

        # Create date range
        start_date = datetime(2022, 1, 1)
        end_date = datetime(2025, 12, 31)
        calendar = pd.DataFrame(
            pd.date_range(start=start_date, end=end_date, freq='D'),
            columns=['date'])

        # Holidays
        holidays = pd.to_datetime(json_data.get('holidays', []))
        holidays_df = pd.DataFrame({'date': holidays, 'is_holiday': 1})

        # Preholidays
        preholidays = pd.to_datetime(json_data.get('preholidays', []))
        preholidays_df = pd.DataFrame({'date': preholidays, 'is_preholiday': 1})

        # Merge DataFrames
        dfs = [calendar, holidays_df, preholidays_df]
        calendar = reduce(
            lambda left, right: pd.merge(left, right, on='date', how='left'),
            dfs)

        calendar[['is_holiday', 'is_preholiday']] = calendar[[
            'is_holiday', 'is_preholiday'
        ]].fillna(0).astype(int)

        return calendar

    def _load_and_prepare_data(self):
        """Loads and prepares the main data, merges with holiday calendar.

        Returns:
            A pd.DataFrame merged with holiday data, sorted by ID and date.

        Raises:
            ValueError: If required columns are missing in the dataset.
        """
        df = self.data.copy()
        required_columns = {self.id, 'day_id'} | set(self.target)
        if not required_columns.issubset(df.columns):
            missing = required_columns - set(df.columns)
            raise ValueError(f"Missing required columns: {missing}")

        df['day_id'] = pd.to_datetime(df['day_id'])

        # Merge with holiday calendar
        df = pd.merge(df, self.calendar, left_on='day_id', right_on='date',
                      how='left')
        df.drop('date', axis=1, inplace=True)

        # Fill missing holiday flags
        df['is_holiday'].fillna(0, inplace=True)
        df['is_preholiday'].fillna(0, inplace=True)
        df[['is_holiday', 'is_preholiday']] = df[[
            'is_holiday', 'is_preholiday'
        ]].astype(int)

        # Sort data
        df = df.sort_values([self.id, 'day_id']).reset_index(drop=True)

        return df

    def _create_features(self):
        """Creates additional features such as lags and calendar-based columns.

        Returns:
            A pd.DataFrame with additional features.
        """
        df = self.df.copy()
        df['day_of_week'] = df['day_id'].dt.dayofweek
        df['month'] = df['day_id'].dt.month
        df['day'] = df['day_id'].dt.day
        df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)

        # Create lag features for each target
        for tgt in self.target:
            df[f'lag_1_{tgt}'] = df.groupby(self.id)[tgt].shift(1)
            df[f'lag_7_{tgt}'] = df.groupby(self.id)[tgt].shift(7)

        # Fill missing values for lag features
        for tgt in self.target:
            df[f'lag_1_{tgt}'].fillna(method='bfill', inplace=True)
            df[f'lag_7_{tgt}'].fillna(method='bfill', inplace=True)

        return df

    def _define_feature_columns(self):
        """Defines which feature columns to use for each target.

        Returns:
            A dictionary with target variables as keys and lists of feature
            column names as values.
        """
        feature_cols_dict = {}
        for tgt in self.target:
            features = [
                'day_of_week',
                'month',
                'day',
                'is_weekend',
                'is_holiday',
                'is_preholiday',
                f'lag_1_{tgt}',
                f'lag_7_{tgt}'
            ]
            feature_cols_dict[tgt] = features
        return feature_cols_dict

    def _create_hybrid_model(self, xgb_params):
        """Creates a hybrid model (Linear Regression + XGBoost).

        Args:
            xgb_params: A dictionary of hyperparameters for XGBoost.

        Returns:
            An instance of the HybridModel class.
        """
        base_model1 = LinearRegression()

        default_params = {
            'n_estimators': 1500,
            'learning_rate': 0.01,
            'max_depth': 12,
            'objective': 'reg:squarederror',
            'random_state': 12345,
            'verbosity': 0
        }

        if xgb_params:
            overlapping_keys = set(default_params.keys()) & set(xgb_params.keys())
            if overlapping_keys:
                self.logger.warning(
                    f"Parameters {overlapping_keys} are overridden by user-defined values."
                )
            default_params.update(xgb_params)

        base_model2 = XGBRegressor(**default_params)
        hybrid_model = HybridModel(base_model1, base_model2)
        return hybrid_model

    def forecast(self):
        """Main method to perform forecasting for each restaurant and target.

        Returns:
            A pd.DataFrame containing forecasts for each target and date.
        """
        self.logger.info("Starting forecast process...")
        results = {tgt: {} for tgt in self.target}
        restaurants = self.df[self.id].unique()
        models = {rest: {tgt: None for tgt in self.target} for rest in restaurants}

        def forecast_restaurant(rest):
            """Helper function to forecast for a single restaurant."""
            rest_df = self.df[self.df[self.id] == rest].copy().reset_index(drop=True)
            last_date = rest_df['day_id'].max()
            future_dates = self._generate_future_dates(last_date)
            future_df = future_dates.copy()
            future_df[self.id] = rest

            restaurant_results = {}
            restaurant_models = {}

            for tgt in self.target:
                self.logger.info(
                    f"Training and forecasting '{tgt}' for restaurant {rest}."
                )
                feature_cols = self.feature_cols_dict[tgt]
                X_train, y_train = rest_df[feature_cols], rest_df[tgt]

                model = self._create_hybrid_model(self.params)
                model.fit(X_train, y_train)
                restaurant_models[tgt] = model
                self.logger.info(
                    f"Model for '{tgt}' and restaurant {rest} has been trained."
                )

                future_df[tgt] = np.nan

                # Iterative forecasting
                for day in range(self.h):
                    lag_1_col = f'lag_1_{tgt}'
                    lag_7_col = f'lag_7_{tgt}'

                    if day == 0:
                        lag_1_value = rest_df.iloc[-1][tgt]
                        if len(rest_df) >= 7:
                            lag_7_value = rest_df.iloc[-7][tgt]
                        else:
                            lag_7_value = rest_df.iloc[-1][tgt]
                    else:
                        lag_1_value = future_df.at[day - 1, tgt]
                        if day >= 7:
                            lag_7_value = future_df.at[day - 7, tgt]
                        else:
                            shift_index = -(7 - day)
                            if (7 - day) > 0 and abs(shift_index) <= len(rest_df):
                                lag_7_value = rest_df.iloc[shift_index][tgt]
                            else:
                                lag_7_value = rest_df.iloc[-1][tgt]

                    current_features = {
                        'day_of_week': future_df.at[day, 'day_of_week'],
                        'month': future_df.at[day, 'month'],
                        'day': future_df.at[day, 'day'],
                        'is_weekend': future_df.at[day, 'is_weekend'],
                        'is_holiday': future_df.at[day, 'is_holiday'],
                        'is_preholiday': future_df.at[day, 'is_preholiday'],
                    }
                    current_features[lag_1_col] = lag_1_value
                    current_features[lag_7_col] = lag_7_value

                    X_current = pd.DataFrame([current_features])
                    y_pred = model.predict(X_current)[0]
                    future_df.at[day, tgt] = y_pred

                restaurant_results[tgt] = future_df[tgt].values
            return rest, restaurant_results, restaurant_models

        if self.tqdm:
            iterator = tqdm(restaurants, desc="Forecasting")
        else:
            iterator = restaurants

        for rest in iterator:
            res = forecast_restaurant(rest)
            rest, restaurant_results, restaurant_models = res
            for tgt in self.target:
                results[tgt][rest] = restaurant_results[tgt]
            models[rest] = restaurant_models

        self.logger.info("Forecasting completed.")
        self.logger.info("Saving forecasts to DataFrame...")
        forecast_df = self._save_forecasts(results, restaurants)
        self.logger.info("Forecasts have been saved.")
        return forecast_df

    def _generate_future_dates(self, last_date):
        """Generates future dates with associated features.

        Args:
            last_date: The last date in the historical data.

        Returns:
            A pd.DataFrame with future dates and calendar-based features.
        """
        future_dates = pd.date_range(
            start=last_date + pd.Timedelta(days=1),
            periods=self.h,
            freq='D'
        )
        future_df = pd.DataFrame({'day_id': future_dates})
        future_df['day_of_week'] = future_df['day_id'].dt.dayofweek
        future_df['month'] = future_df['day_id'].dt.month
        future_df['day'] = future_df['day_id'].dt.day
        future_df['is_weekend'] = future_df['day_of_week'].isin([5, 6]).astype(int)

        # Merge with holiday calendar
        future_df = pd.merge(future_df,
                             self.calendar,
                             left_on='day_id',
                             right_on='date',
                             how='left')
        future_df.drop('date', axis=1, inplace=True)
        future_df['is_holiday'].fillna(0, inplace=True)
        future_df['is_preholiday'].fillna(0, inplace=True)
        future_df[['is_holiday', 'is_preholiday']] = future_df[[
            'is_holiday', 'is_preholiday'
        ]].astype(int)

        return future_df

    def _save_forecasts(self, results, restaurants):
        """Saves forecasts in a DataFrame format.

        Args:
            results: A dictionary containing forecasts for each target and restaurant.
            restaurants: An array-like object of restaurant IDs.

        Returns:
            A pd.DataFrame with columns [rest_id, day_id, sales, check_qnty, ...].
        """
        forecast_list = []
        for tgt in self.target:
            for rest in restaurants:
                last_date = self.df[self.df[self.id] == rest]['day_id'].max()
                future_dates = pd.date_range(
                    start=last_date + pd.Timedelta(days=1),
                    periods=self.h,
                    freq='D'
                )
                forecasts = results[tgt][rest]
                for date, value in zip(future_dates, forecasts):
                    forecast_list.append({
                        self.id: rest,
                        'day_id': date,
                        'target': tgt,
                        'forecast': value
                    })

        forecast = pd.DataFrame(forecast_list)
        data = forecast.pivot(index=['rest_id', 'day_id'],
                              columns='target',
                              values='forecast').reset_index()
        data.rename_axis(None, axis=1, inplace=True)
        return data