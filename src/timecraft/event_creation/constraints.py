from abc import ABC, abstractmethod
from enum import Enum
from typing import List

from timecraft.event_creation.event import Class


class Constraint(ABC):
    class ConstraintType(Enum):
        hard = "hard"
        soft = "soft"

    def __init__(self, Constraint_type: ConstraintType):
        self.Constraint_type = Constraint_type

    @abstractmethod
    def calculate_fitness(self):
        pass


class FacultyOverlapConstraint(Constraint):
    def __init__(self):
        super().__init__(Constraint_type=super().ConstraintType("hard"))

    def calculate_fitness(
        self, genome: List[List[int]], classes: List[Class], fixed_slots: List[int]
    ):
        fitness = 0
        for i, fixed_slot in enumerate(fixed_slots):
            for j in range(len(genome)):
                faculty_occupied_slots = (
                    classes[genome[j][i]].faculties[0].occupied_slots
                )
                if faculty_occupied_slots and fixed_slot in faculty_occupied_slots:
                    fitness += 1
        return fitness
