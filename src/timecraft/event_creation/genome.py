from timecraft.event_creation.event import Class
from timecraft.models import Course, Faculty
from timecraft.event_creation.constraints import (
    FacultyOverlapConstraint,
    HourConstraint,
    ColumnRedundancyConstraint,
)
from typing import List

from numpy.random import choice

from icecream import ic


class Genome:
    def __init__(self, courses: List[Course], fixed_slots: List[int]):
        self.courses = courses
        self._fixed_slots = fixed_slots
        self.genome = []
        self._classes = []
        self._classes_by_course_code: dict[str, List[int]] = None
        self.constraints = [
            FacultyOverlapConstraint(),
            HourConstraint(),
            ColumnRedundancyConstraint(),
        ]
        self._fitness_score = -1

    @property
    def fixed_slots(self):
        return self._fixed_slots if self._fixed_slots else []

    @property
    def classes_by_course_code(self):
        if self._classes_by_course_code is None:
            self._classes_by_course_code = {c.code: [] for c in self.courses}
            for course in self.courses:
                if not course.faculty_hour_split:
                    self._classes.append(
                        Class(
                            course_code=course.code,
                            faculties=course.faculties,
                            no_hours=course.no_hours,
                        )
                    )
                    self._classes_by_course_code[course.code].append(
                        len(self._classes) - 1
                    )
                else:
                    for i, faculty in enumerate(course.faculties):
                        self._classes.append(
                            Class(
                                course_code=course.code,
                                faculties=[faculty],
                                no_hours=course.faculty_hour_split[i],
                            )
                        )
                        self._classes_by_course_code[course.code].append(
                            len(self._classes) - 1
                        )
        return self._classes_by_course_code

    @property
    def no_hours(self):
        return self.courses[0].no_hours

    def initialize(self):
        for classes in self.classes_by_course_code.values():
            self.genome.append(list(choice(classes, size=self.no_hours)))
        return self

    @property
    def fitness_score(self):
        if self._fitness_score == -1:
            self._fitness_score = self._calculate_fitness_score()
        return self._fitness_score

    def _calculate_fitness_score(self):
        fitness_score = 0
        hard_fitness_score = sum(
            constraint.calculate_fitness_score(
                genome=self.genome,
                classes=self._classes,
                fixed_slots=self.fixed_slots,
            )
            for constraint in self.constraints
            if constraint.type.value == "hard"
        )
        fitness_score += 1 / (1 + hard_fitness_score)
        if not hard_fitness_score:
            soft_fitness_score = sum(
                constraint.calculate_fitness_score(
                    genome=self.genome,
                    classes=self._classes,
                    fixed_slots=self.fixed_slots,
                )
                for constraint in self.constraints
                if constraint.type.value == "soft"
            )
            fitness_score += 1 / (1 + soft_fitness_score)
        return fitness_score


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
    genome = Genome(courses=courses, fixed_slots=None).initialize()
    ic(genome.genome, genome.fitness_score)


main()
