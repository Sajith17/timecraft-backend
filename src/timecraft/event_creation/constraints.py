from abc import ABC, abstractmethod
from enum import Enum
from typing import List
from icecream import ic

from timecraft.event_creation.event import Class, DataHelper


class Constraint(ABC):
    class Type(Enum):
        hard = "hard"
        soft = "soft"

    def __init__(self, type: Type):
        self.type = type

    @abstractmethod
    def calculate_fitness_score(self):
        pass


class HourConstraint(Constraint):
    def __init__(self, data_helper: DataHelper):
        super().__init__(type=super().Type("hard"))
        self.data_helper = data_helper

    def calculate_fitness_score(self, assignment: List[List[int]]):
        fitness_score = 0
        for row in assignment:
            hours_by_class_index = dict()
            for class_index in row:
                if class_index in hours_by_class_index:
                    hours_by_class_index[class_index] += 1
                else:
                    hours_by_class_index[class_index] = 1
            fitness_score += sum(
                max(hours - self.data_helper.classes[class_index].no_hours, 0)
                for class_index, hours in hours_by_class_index.items()
            )
        # ic("hour constraint", fitness_score)
        return fitness_score


class FacultyOverlapConstraint(Constraint):
    def __init__(self, data_helper: DataHelper):
        super().__init__(type=super().Type("hard"))
        self.data_helper = data_helper

    def calculate_fitness_score(self, assignment: List[List[int]]):
        fitness_score = 0
        for i, fixed_slot in enumerate(self.data_helper.fixed_slots):
            for j in range(len(assignment)):
                faculty_occupied_slots = (
                    self.data_helper.classes[assignment[j][i]]
                    .faculties[0]
                    .occupied_slots
                )
                if faculty_occupied_slots and fixed_slot in faculty_occupied_slots:
                    fitness_score += 1
        # ic("FacultyOverlapConstraint", fitness_score)
        return fitness_score


class ColumnRedundancyConstraint(Constraint):
    """This constraint is used to minimize the number of unique columns which then results in minimized number of event creation."""

    def __init__(self, data_helper: DataHelper):
        super().__init__(type=super().Type("soft"))
        self.data_helper = data_helper

    def calculate_fitness_score(self, assignment: List[List[int]]):
        fitness_score = len(
            set(
                tuple(assignment[i][column_index] for i in range(len(assignment)))
                for column_index in range(
                    len(self.data_helper.fixed_slots), len(assignment[0])
                )
            )
        )
        # ic("ColumnRedundancyConstraint", fitness_score)
        return fitness_score
