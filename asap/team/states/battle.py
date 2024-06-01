from dataclasses import dataclass

from asap.team.team import Team


@dataclass
class TeamBattleState:
    team: Team
