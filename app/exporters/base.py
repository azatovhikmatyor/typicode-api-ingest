from abc import ABC, abstractmethod
from typing import Union, Sequence, Mapping
from .. import functions as fn

class Exporter(ABC):
    @abstractmethod
    def export(self, data) -> None:
        pass


class ExportableFlattenedJson:
    def __init__(self, data: Union[Sequence, Mapping], exporter: Exporter) -> None:
        self.exporter = exporter
        if fn.is_nested(data):
            self.data = fn.flatten_json_list(data)
        else:
            self.data = data

    def export(self) -> None:
        self.exporter.export(self.data)
