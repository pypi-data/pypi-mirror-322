from dataclasses import dataclass
from typing import Type


@dataclass(frozen=True)
class Property:
    label: str
    datatype: Type
    postfix: str | None = None

    def final_assigment(self, parent_node_return_id: str):
        return f"{parent_node_return_id}{self.postfix or ''}"

    def cypher_assigment(self, parent_node_return_id: str):
        return f"{parent_node_return_id}.{self.label}"
