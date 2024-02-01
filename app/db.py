import sqlite3


class SqliteTable:
    def __init__(self, table_name: str, db_name: str):
        self.table_name = table_name
        self.db_name = db_name

    def truncate(self):
        truncate_table_statement = f"DELETE FROM {self.table_name}"
        self._execute(truncate_table_statement)

    def create_if_not_exists(self, sample_row):
        columns = []

        for key, value in sample_row.items():
            column_type = self._sqlite_type(value)
            columns.append(f"{key} {column_type}")

        columns = ",\n\t".join(columns)
        create_table_statement = (
            f"create table if not exists {self.table_name} (\n{columns}\n);"
        )

        print(create_table_statement)
        self._execute(create_table_statement)

    def insert(self, data):
        if len(data) == 0:
            return

        args = ", ".join((":" + key for key in data[0].keys()))
        stmt = f"INSERT INTO {self.table_name}({', '.join(data[0].keys())}) VALUES ({args})"
        with sqlite3.connect(self.db_name) as con:
            con.executemany(stmt, data)
            con.commit()

    @staticmethod
    def _sqlite_type(value):
        if isinstance(value, int):
            return "integer"
        elif isinstance(value, float):
            return "real"
        elif isinstance(value, str):
            return "text"
        elif isinstance(value, bytes):
            return "blob"
        else:
            return "text"  # Default to text for unknown types

    def _execute(self, stmt):
        with sqlite3.connect(self.db_name) as con:
            con.execute(stmt)
            con.commit()
