import re
import pandas as pd

class ColumnCleaner:
    def __init__(self, df: pd.DataFrame, case: str = 'snake', remove_special: bool = True):
        """
        Initializes the ColumnCleaner instance by cleaning the DataFrame's column names.

        :param df: The original pandas DataFrame.
        :param case: The desired case style for column names. Options:
                     'snake' - snake_case,
                     'camel' - camelCase,
                     'title' - Title Case.
        :param remove_special: Whether to remove special characters from column names.
        """
        # Assertions to ensure correct input types and values
        assert isinstance(df, pd.DataFrame), "df must be a pandas DataFrame."
        assert case in ['snake', 'camel', 'title'], "case must be one of 'snake', 'camel', or 'title'."
        assert isinstance(remove_special, bool), "remove_special must be a boolean."

        self.case = case
        self.remove_special = remove_special
        self.df = self._clean_columns(df)

    def _to_snake_case(self, name: str) -> str:
        """
        Converts a string to snake_case.

        :param name: The original column name.
        :return: The column name in snake_case.
        """
        name = re.sub(r'[\s\-]+', '_', name)  # Replace spaces and hyphens with underscores
        name = re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()  # Insert underscores before uppercase letters
        return name

    def _to_camel_case(self, name: str) -> str:
        """
        Converts a string to camelCase.

        :param name: The original column name.
        :return: The column name in camelCase.
        """
        parts = re.split(r'[\s\-_]+', name)
        assert len(parts) > 0, "Column name must contain at least one character."
        return parts[0].lower() + ''.join(word.capitalize() for word in parts[1:])

    def _to_title_case(self, name: str) -> str:
        """
        Converts a string to Title Case.

        :param name: The original column name.
        :return: The column name in Title Case.
        """
        return ' '.join(word.capitalize() for word in re.split(r'[\s\-_]+', name))

    def _clean_column_name(self, name: str) -> str:
        """
        Cleans a single column name based on the specified case and special character removal.

        :param name: The original column name.
        :return: The cleaned column name.
        """
        assert isinstance(name, str), "Column names must be strings."

        if self.remove_special:
            name = re.sub(r'[^\w\s\-]', '', name)  # Remove all except letters, numbers, spaces, and hyphens

        if self.case == 'snake':
            cleaned_name = self._to_snake_case(name)
        elif self.case == 'camel':
            cleaned_name = self._to_camel_case(name)
        elif self.case == 'title':
            cleaned_name = self._to_title_case(name)
        else:
            raise ValueError("Unsupported case style. Choose from 'snake', 'camel', 'title'.")

        assert isinstance(cleaned_name, str) and cleaned_name, "Cleaned column name must be a non-empty string."
        return cleaned_name

    def _clean_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Cleans all column names in the DataFrame.

        :param df: The original pandas DataFrame.
        :return: A new DataFrame with cleaned column names.
        """
        df = df.copy()
        df.columns = [self._clean_column_name(col) for col in df.columns]
        return df

    def __getattr__(self, attr):
        """
        Redirects attribute access to the internal DataFrame.

        :param attr: The attribute to access.
        :return: The attribute from the internal DataFrame.
        """
        return getattr(self.df, attr)

    def __repr__(self):
        """
        Returns the official string representation of the ColumnCleaner instance.

        :return: The string representation of the internal DataFrame.
        """
        return repr(self.df)

    def __str__(self):
        """
        Returns the informal string representation of the ColumnCleaner instance.

        :return: The string representation of the internal DataFrame.
        """
        return str(self.df)