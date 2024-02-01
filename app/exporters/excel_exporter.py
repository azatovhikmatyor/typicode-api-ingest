from .base import Exporter

# TODO: ExcelExported not implemented yet
class ExcelExporter(Exporter):
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name

    def export(self, data) -> None:
        raise NotImplementedError("Not Implementd Yet")
