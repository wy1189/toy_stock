# -*- coding:utf-8 -*-
# @Filename:    name_converter.py
# @Author:      woojong
# @Time:        2/6/22 10:41 PM

import random
import sqlite3
import string
import pandas as pd

from datetime import datetime
from pathlib import Path
from typing import List


class FileNameGenerator:
    """
    A file name generator based on random alphanumeric strings with length (default is 100)
    This class is intended to convert long string into pseudo random string with a specific length.
    """
    def __init__(self, db_path: Path = None, table_name: str = "file_name_map", length: int = 100) -> None:
        """
        :param db_path: (Path) full path of sqlite3 db
        :param table_name: (str) table name to be generated
        """
        # if db_path is missing, value error
        if db_path is None:
            raise ValueError("You must include a path for db.")

        # initialize sqlite3.connect and cursor
        self.connect = self.cursor = None

        # set class variables
        self.table_name = table_name
        self.db_name = db_path
        self.length = length
        self.id_col = "original_name"
        self.encrypt_col = "converted_name"
        self.date_col = "date_time"

        # set connect and cursor
        self.connect_db()

        # create table if not exist
        create_query = f"""
        -- id: original string
        -- file_name: converted file name
        -- date: date and time for the converted file name
        CREATE TABLE IF NOT EXISTS {self.table_name}(
            {self.id_col} text NOT NULL,
            {self.encrypt_col} text NOT NULL,
            {self.date_col} text
        );
        """

        # generate table
        self.run_query(create_query)

    def connect_db(self) -> None:
        """connect to db"""
        self.connect = sqlite3.connect(self.db_name)
        self.cursor = self.connect.cursor()

    def run_query(self, query: str) -> None:
        """
        execute query
        :param query:
        :return:
        """
        self.cursor.execute(query)

    def insert_db(self, column_id: str) -> None:
        """

        :param column_id: (str) column id to be compared
        :return: insert row if id is not included in the table
        """
        query = self.insert_query(column_id)
        self.run_query(query)
        self.connect.commit()

    def insert_query(self, column_id: str, user_random: str = None) -> str:
        random_string = user_random
        if user_random is None:
            random_check = True
            while random_check:
                random_string = self.random_alphanumeric(self.length)
                sql_result = self.cursor.execute(
                    f"SELECT {self.encrypt_col} FROM {self.table_name} WHERE {self.encrypt_col} = '{random_string}'"
                )
                random_check = sql_result.fetchall()
        else:
            sql_result = self.cursor.execute(
                f"SELECT {self.encrypt_col} FROM {self.table_name} WHERE {self.encrypt_col} = '{random_string}'"
            )
            random_check = sql_result.fetchall()
            if random_check:
                raise ValueError("User random string is not unique.")

        query = f"""
        INSERT INTO {self.table_name} ({self.id_col}, {self.encrypt_col}, {self.date_col}) 
        SELECT '{column_id}', '{random_string}', '{datetime.now().strftime("%Y-%m-%d %H-%M-%S")}' 
        WHERE NOT EXISTS(SELECT {self.id_col} FROM {self.table_name} WHERE {self.id_col} = '{column_id}');
        """
        return query

    def retrieve_db(self, column_id: str) -> List[tuple]:
        query = self.retrieve_query(column_id)
        self.run_query(query)
        return self.cursor.fetchall()

    def retrieve_query(self, column_id: str) -> str:
        query = f"SELECT * FROM {self.table_name} WHERE {self.id_col} = '{column_id}'"
        return query

    def close_db(self) -> None:
        self.connect.close()

    @staticmethod
    def random_alphanumeric(length: int = 100) -> str:
        """
        generate random alphanumeric string (case sensitive)
        :param length: (int) the fixed length of output string
        :return: (str)
        """
        random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        return random_str


if __name__ == "__main__":
    url_query = "company_id=co766"
    url_query2 = "company_id=co766&hotel_id=ho3366"

    base_path = Path("/Users/woojong/Desktop/redis/")
    db_name = datetime.today().strftime("%Y-%m-%d") + "_sqlite.db"
    date_path = base_path / db_name

    name_generator = FileNameGenerator(date_path)
    try:
        print(name_generator.insert_query(url_query,
                                          "AryhqzXnp2Q7dG27TH3lab7IsqKeBwM7Ffxn86r1CJ4Dwbd9YMhMkHDiX5iBp3czynRiGAiG78jHkToG8bdJ8pNdpBzOvfa2sGUa"))
    except:
        print("value error?")
        name_generator.insert_db(url_query)
        name_generator.cursor.execute(name_generator.retrieve_query(url_query))
        temp = name_generator.cursor.fetchone()
        print(temp[1])
        name_generator.retrieve_db(url_query)

        name_generator.insert_db(url_query2)
        name_generator.cursor.execute(name_generator.retrieve_query(url_query2))
        temp = name_generator.cursor.fetchone()
        print(temp[1])
        name_generator.retrieve_db(url_query2)
        name_generator.connect.close()
        name_generator.connect_db()

        con = sqlite3.connect("/Users/woojong/Desktop/redis/2022-02-06_sqlite.db")

        print(pd.read_sql_query("SELECT * FROM file_id;", con))