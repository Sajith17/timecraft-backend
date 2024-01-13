from abc import ABC, abstractmethod
from enum import Enum
from typing import List
from icecream import ic

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


class HourConstraint(Constraint):
    def __init__(self):
        super().__init__(Constraint_type=super().ConstraintType("hard"))

    def calculate_fitness(
        self, genome: List[List[int]], classes: List[Class], fixed_slots: List[int]
    ):
        fitness = 0
        for row in genome:
            hours_by_class_index = dict()
            for class_index in row:
                if class_index in hours_by_class_index:
                    hours_by_class_index[class_index] += 1
                else:
                    hours_by_class_index[class_index] = 1
            fitness += sum(
                max(hours - classes[class_index].no_hours, 0)
                for class_index, hours in hours_by_class_index.items()
            )
        return fitness


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


class ColumnRedundancyConstraint(Constraint):
    """This constraint is used to minimize the number of unique columns which then results in minimized number of event creation."""

    def __init__(self):
        super().__init__(Constraint_type=super().ConstraintType("soft"))

    def calculate_fitness(
        self, genome: List[List[int]], classes: List[Class], fixed_slots: List[int]
    ):
        fitness = len(
            set(
                tuple(genome[i][column_index] for i in range(len(genome)))
                for column_index in range(len(fixed_slots), len(genome[0]))
            )
        )
        return fitness
