from dataclasses import dataclass
from typing import Dict, Literal


@dataclass
class UrlDateFilter:
    attribute: str
    operator: Literal[">", "<", "<=", ">="]
    value: str

    def _map_operator_literal_to_str(self):
        match self.operator:
            case ">":
                return "gt"
            case ">=":
                return "gte"
            case "<":
                return "lt"
            case "<=":
                return "lte"

    def serialize(self) -> Dict[str, str]:
        key = f"where[{self.attribute}][{self._map_operator_literal_to_str()}]"
        return {key: self.value}
