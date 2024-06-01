from dataclasses import dataclass

from asap.engine.team.team import Team


@dataclass
class TeamBattleState:
    team: Team
