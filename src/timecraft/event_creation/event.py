from __future__ import annotations
from dataclasses import dataclass
from typing import List,Optional
from timecraft.models import Course, Faculty

from icecream import ic


@dataclass(frozen=True)
class Class:
    course_code: str
    faculties: List[Faculty]
    no_hours: int

    @property
    def faculty_codes(self):
        return [f.code for f in self.faculties]

    @classmethod
    def create_classes_from_courses(cls, courses: List[Course]) -> List[Class]:
        classes = []
        for course in courses:
            if not course.faculty_hour_split:
                classes.append(
                    Class(
                        course_code=course.code,
                        faculties=course.faculties,
                        no_hours=course.no_hours,
                    )
                )
            else:
                for i, faculty in enumerate(course.faculties):
                    classes.append(
                        Class(
                            course_code=course.code,
                            faculties=[faculty],
                            no_hours=course.faculty_hour_split[i],
                        )
                    )
        return classes


@dataclass(slots=True)
class Event:
    classes: List[Class]
    no_hours: int
    student_group: str
    fixed_slots: Optional[List[int]] = None
    _course_codes: Optional[List[str]] = None
    _faculty_codes: Optional[List[str]] = None

    @property
    def course_codes(self):
        if not self._course_codes:
            self._course_codes = [c.course.code for c in self.classes]
        return self._course_codes

    @property
    def faculty_codes(self):
        if not self._faculty_codes:
            self._faculty_codes = []
            for c in self.classes:
                self._faculty_codes += c.faculty_codes
        return self._faculty_codes


def main():
    courses = [
        Course(
            code="CS101",
            faculties=[Faculty(code="MATH1"), Faculty(code="MATH2")],
            no_hours=5,
            student_group="A",
            faculty_hour_split=[1, 4],
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


if __name__ == "__main__":
    main()
