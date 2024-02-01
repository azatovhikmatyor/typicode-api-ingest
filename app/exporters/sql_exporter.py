from .base import Exporter
from ..db import SqliteTable

# NOTE: only sqlite database supported for now


class SqliteExporter(Exporter):
    def __init__(self, table_name: str, db_name: str) -> None:
        self.table_name = table_name
        self.db_name = db_name
        self.table = SqliteTable(table_name, db_name)

    def export(self, data) -> None:
        if len(data) == 0:
            return
        self.table.create_if_not_exists(sample_row=data[0])
        self.table.truncate()  # for only full load
        self.table.insert(data)
