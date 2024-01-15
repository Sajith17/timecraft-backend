from timecraft.event_creation.event import Class
from timecraft.models import Course, Faculty
from timecraft.event_creation.constraints import (
    FacultyOverlapConstraint,
    HourConstraint,
    ColumnRedundancyConstraint,
)
from timecraft.event_creation.fitness_calculator import FitnessCalculator
from typing import List, Dict
from numpy.random import choice
from icecream import ic


class Genome:
    def __init__(
        self, classes: List[Class], no_slots: int, fixed_slots: List[int] | None
    ):
        self.classes = classes
        self.no_slots = no_slots
        self.fixed_slots = fixed_slots if fixed_slots else []
        self._classes_by_course_code: Dict[str, List[int]] | None = None
        self.assignment = []
        self.fitness_calculator = FitnessCalculator(
            constraints=[
                FacultyOverlapConstraint(),
                HourConstraint(),
                ColumnRedundancyConstraint(),
            ]
        )
        self._fitness_score = -1

    def initialize(self):
        for classes in self.classes_by_course_code.values():
            self.assignment.append(list(choice(a=classes, size=self.no_slots)))  # type: ignore
        return self

    @property
    def classes_by_course_code(self):
        if self._classes_by_course_code is None:
            self._classes_by_course_code = {}
            for i, c in enumerate(self.classes):
                if c.course_code in self._classes_by_course_code:
                    self._classes_by_course_code[c.course_code].append(i)
                else:
                    self._classes_by_course_code[c.course_code] = [i]
        return self._classes_by_course_code

    @property
    def fitness_score(self):
        if self._fitness_score == -1:
            self._fitness_score = self.fitness_calculator.calculate_score(
                assignment=self.assignment,
                classes=self.classes,
                fixed_slots=self.fixed_slots,
            )
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
    genome = Genome(classes=classes, no_slots=no_slots, fixed_slots=None).initialize()
    ic(genome.assignment)
    ic(genome.fitness_score)


if __name__ == "__main__":
    main()
