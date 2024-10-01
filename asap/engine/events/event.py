import enum
from dataclasses import dataclass
from typing import Optional


@dataclass
class Event:
    class Type(enum.Enum):
        HURT = 1
        FAINT = 2
        KNOCKOUT = 3

    type: Type
    target: 'Pet'
    source: 'Pet'
    delta_attack: Optional[int] = 0
    delta_health: Optional[int] = 0

    def execute(self):
        self.target.extra_attack += self.delta_attack
        self.target.extra_health += self.delta_health


HURT = Event.Type.HURT
FAINT = Event.Type.FAINT
KNOCKOUT = Event.Type.KNOCKOUT
