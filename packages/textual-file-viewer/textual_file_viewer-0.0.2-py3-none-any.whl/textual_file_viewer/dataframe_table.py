# https://github.com/dannywade/textual-pandas
from typing import Any

from textual.widgets import DataTable
import pandas as pd


class DataFrameTable(DataTable):
    """Display Pandas dataframe in DataTable widget."""

    DEFAULT_CSS = """
    DataFrameTable {
        height: 1fr
    }
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.df = pd.DataFrame()

    def add_df(self, df: pd.DataFrame):
        """Add DataFrame data to DataTable."""
        self.df = df
        self.add_columns(*self._get_df_columns())
        self.add_rows(self._get_df_rows()[0:])
        return self

    def update_df(self, df: pd.DataFrame):
        """Update DataFrameTable with a new DataFrame."""
        # Clear existing datatable
        self.clear(columns=True)
        # Redraw table with new dataframe
        self.add_df(df)

    def _get_df_rows(self) -> list[tuple]:
        """Convert dataframe rows to iterable."""
        return list(self.df.itertuples(index=False, name=None))

    def _get_df_columns(self) -> tuple:
        """Extract column names from dataframe."""
        return tuple(self.df.columns.values.tolist())