#!/usr/bin/env python3
"""
Test Pandas DataFrame loaders.
"""

import pathlib
import sqlite3
import tempfile
import unittest

import pandas as pd

from dalood.exception import LoaderValueError
from dalood.loader.pandas import DataFrameCSVLoader, DataFrameSQLLoader
from dalood.manager import Manager


from test_dalood.utils import tmp_file


CSV_EXT = ".csv"


class TestDataFrameCSV(unittest.TestCase):
    """
    Test Pandas DataFrame loading from CSV files.
    """

    def setUp(self):
        self.data = pd.DataFrame({"number": [1, 2, 3], "letter": ["a", "b", "c"]})
        self.tmp_file_ctx = tmp_file(
            text=self.data.to_csv(index=False), extension=CSV_EXT
        )
        self.man = Manager()
        self.man.register_loader(
            f"*{CSV_EXT}", DataFrameCSVLoader(), pattern_type="glob"
        )

    def test_csv_file_load(self):
        """
        Pandas DataFrame is loaded from file.
        """
        with self.tmp_file_ctx as (_, _, path):
            self.assertTrue(self.data.equals(self.man.get(path)))

    def test_same_object(self):
        """
        Manager returns the same object on subsequent calls.
        """
        with self.tmp_file_ctx as (_, _, path):
            self.assertIs(self.man.get(path), self.man.get(path))

    def test_patterns(self):
        """
        Pandas file loader registers its own patterns.
        """
        man = Manager()
        loader = DataFrameCSVLoader()
        with self.tmp_file_ctx as (_, _, path):
            with self.assertRaises(LoaderValueError):
                man.get(path.as_uri())

            loader.register_patterns(man)
            self.assertTrue(self.data.equals(man.get(path)))


class TestDataFrameSQL(unittest.TestCase):
    """
    Test Pandas DataFrame loading from SQL databases.
    """

    def setUp(self):
        self.tmp_dir_obj = (
            tempfile.TemporaryDirectory()  # pylint: disable=consider-using-with
        )
        self.db_path = pathlib.Path(self.tmp_dir_obj.name) / "db.sqlite3"
        self.data = pd.DataFrame({"number": [1, 2, 3], "letter": ["a", "b", "c"]})
        self.table_name = "test"

        conn = sqlite3.connect(self.db_path)
        self.data.to_sql(self.table_name, conn, index=False)

        self.man = Manager()
        self.loader = DataFrameSQLLoader(con=conn)
        self.loader.map("sqltest", f"SELECT * FROM {self.table_name}")
        self.loader.register_patterns(self.man)

    def tearDown(self):
        self.tmp_dir_obj.cleanup()

    def test_sql_load(self):
        """
        Pandas DataFrame is loaded from SQL.
        """
        self.assertTrue(self.data.equals(self.man.get("sqltest")))

    def test_map(self):
        """
        New sources are mapped to new SQL statements.
        """
        self.loader.map("sqltest", f"SELECT letter FROM {self.table_name}")
        self.assertTrue(
            self.data.drop(["number"], axis=1).equals(self.man.get("sqltest"))
        )


if __name__ == "__main__":
    unittest.main()
