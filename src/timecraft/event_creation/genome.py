from timecraft.event_creation.event import Class, DataHelper
from timecraft.models import Course, Faculty
from timecraft.event_creation.constraints import (
    FacultyOverlapConstraint,
    HourConstraint,
    ColumnRedundancyConstraint,
    Constraint,
)
from timecraft.event_creation.fitness_calculator import FitnessCalculator
from typing import List, Dict
from numpy.random import choice
from icecream import ic


class Genome:
    def __init__(self, data_helper: DataHelper, constraints: List[Constraint] = []):
        self.data_helper = data_helper
        self.assignment = []
        self.fitness_calculator = FitnessCalculator(constraints=constraints)
        self.if_fitness_changed = False
        self._fitness_score = -1

    def initialize(self):
        for classes in self.data_helper.classes_by_course_code.values():
            self.assignment.append(list(choice(a=classes, size=self.data_helper.no_slots)))  # type: ignore
        return self

    @property
    def fitness_score(self):
        if self._fitness_score == -1 or self.if_fitness_changed:
            self._fitness_score = self.fitness_calculator.calculate_score(
                assignment=self.assignment
            )
            self.if_fitness_changed = False
        return self._fitness_score


def main():
    courses = [
        Course(
            code="CS101",
            faculties=[Faculty(code="MATH1"), Faculty(code="MATH2")],
            no_hours=5,
            student_group="A",
        ),
        Course(
            code="CS102",
            faculties=[Faculty(code="MATH3"), Faculty(code="MATH4")],
            no_hours=5,
            student_group="A",
            faculty_hour_split=[2, 3],
        ),
    ]
    classes = Class.create_classes_from_courses(courses=courses)
    no_slots = courses[0].no_hours
    data_helper = DataHelper(classes=classes, no_slots=no_slots)
    constraints = [
        FacultyOverlapConstraint(data_helper=data_helper),
        HourConstraint(data_helper=data_helper),
        ColumnRedundancyConstraint(data_helper=data_helper),
    ]
    genome = Genome(data_helper=data_helper, constraints=constraints).initialize()
    ic(genome.assignment)
    ic(genome.fitness_score)


if __name__ == "__main__":
    main()
