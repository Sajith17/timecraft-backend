from dataclasses import dataclass
from typing import List, Optional
from timecraft.models import Course, Faculty
from timecraft.utils import convert_keys
from icecream import ic


@dataclass(slots=True, frozen=True)
class Class:
    course: Course
    faculties: List[Faculty]

    @property
    def faculty_codes(self):
        return [f.code for f in self.faculties]


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
    event = Event(
        classes=[
            Class(
                course=Course(
                    code="CS101",
                    name="Computer Science 1",
                    faculties=[
                        Faculty(
                            code="CS", name="Computer Science", occupied_slots=[1, 2, 3]
                        )
                    ],
                    no_hours=8,
                    student_group="A",
                ),
                faculties=[Faculty(code="CS", name="Computer Science")],
            ),
            Class(
                course=Course(
                    code="CS201",
                    name="Computer Science 2",
                    faculties=[Faculty(code="CS", name="Computer Science")],
                    no_hours=8,
                    student_group="B",
                ),
                faculties=[Faculty(code="CS", name="Computer Science")],
            ),
        ],
        no_hours=16,
        student_group="All",
        fixed_slots=[1, 2, 3],
    )
    ic(event.faculty_codes, event.course_codes)


if __name__ == "__main__":
    main()
