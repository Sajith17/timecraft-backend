from timecraft.event_creation.event import Class
from timecraft.models import JointCourses, Course, Faculty
from typing import List

from numpy.random import choice

from icecream import ic


class Genome:
    def __init__(self, joint_courses: JointCourses):
        self.courses = joint_courses.courses
        self.fixed_slots = joint_courses.fixed_slots
        self.genome = []
        self._classes = []
        self._classes_by_course_code: dict[str, List[int]] = None
        self.fitness = -1

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


def main():
    joint_courses = JointCourses(
        courses=[
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
    )
    genome1 = Genome(joint_courses=joint_courses)
    ic(genome1.initialize().genome)


if __name__ == "__main__":
    main()
