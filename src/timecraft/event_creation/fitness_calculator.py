from timecraft.event_creation.constraints import Constraint
from timecraft.event_creation.event import Class
from typing import List

from icecream import ic


class FitnessCalculator:
    def __init__(self, constraints: List[Constraint]):
        self.constraints = constraints

    def calculate_score(self, assignment: List[List[int]]) -> float:
        fitness_score = 0
        fitness_score += self.scale(
            sum(
                constraint.calculate_fitness_score(assignment=assignment)
                for constraint in self.hard_constraints
            )
        )
        if fitness_score == 1:
            fitness_score += self.scale(
                sum(
                    constraint.calculate_fitness_score(assignment=assignment)
                    for constraint in self.soft_constraints
                )
            )
        return fitness_score

    @property
    def hard_constraints(self) -> List[Constraint]:
        return [
            constraint
            for constraint in self.constraints
            if constraint.type == constraint.Type.HARD
        ]

    @property
    def soft_constraints(self) -> List[Constraint]:
        return [
            constraint
            for constraint in self.constraints
            if constraint.type == constraint.Type.SOFT
        ]

    @staticmethod
    def scale(x: int) -> float:
        return 1 / (1.0 + x)
