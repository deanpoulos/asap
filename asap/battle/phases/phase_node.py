from typing import Dict, Callable


class PhaseNode:
    def __init__(self):
        self.phase_name: str = ""
        self.edges: Dict[Callable, PhaseNode] = {}

    def add_edge(self, condition: Callable, node: 'PhaseNode'):
        self.edges[condition] = node

    def __repr__(self):
        return f"{self.phase_name}"
