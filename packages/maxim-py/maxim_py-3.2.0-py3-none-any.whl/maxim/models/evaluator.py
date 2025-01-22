from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional


@dataclass
class EvaluatorType(Enum):
    AI = "AI"
    PROGRAMMATIC = "Programmatic"
    STATISTICAL = "Statistical"
    API = "API"
    HUMAN = "Human"
    THIRD_PARTY = "ThirdParty"


@dataclass
class Evaluator:
    id: str
    name: str
    type: EvaluatorType
    builtin: bool
    reversed: Optional[bool] = False

    def __json__(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "builtin": self.builtin,
            "reversed": self.reversed,
        }

    @classmethod
    def dict_to_class(cls, data: Dict[str, Any]) -> "Evaluator":
        return cls(
            id=data["id"],
            name=data["name"],
            type=data["type"],
            builtin=data["builtin"],
            reversed=data.get("reversed"),
        )
