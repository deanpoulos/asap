import enum
from dataclasses import dataclass
from typing import Optional


@dataclass
class Event:
    class Type(enum.Enum):
        HURT = 1
        FAINT = 2

    type: Type
    target: 'Pet'
    source: 'Pet'
    delta_attack: Optional[int] = 0
    delta_health: Optional[int] = 0
