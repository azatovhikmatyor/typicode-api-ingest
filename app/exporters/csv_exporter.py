from .base import Exporter
import csv


class CsvExporter(Exporter):
    def __init__(self, filename: str) -> None:
        self.filename = filename

    def export(self, data) -> None:
        if len(data) == 0:
            return

        fields = data[0].keys()  # Assuming all dictionaries have the same keys
        with open(self.filename, "wt", encoding="utf8", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fields)
            writer.writeheader()
            writer.writerows(data)
