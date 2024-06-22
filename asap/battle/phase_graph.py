from asap.battle.phases.phase_node import PhaseNode


class DirectedAcyclicPhaseGraph:
    def __init__(self, root: PhaseNode):
        """
        Acyclic graph of pet-event phases, where each node is a phase
        and each edge is a condition which must be met to transition
        to the next phases.
        """
        self.root = root