from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional
from timecraft.models import Course, Faculty, Assignment
from timecraft.utils import convert_keys


import json
from icecream import ic


@dataclass(frozen=True, slots=True)
class Event:
    courses: List[Course]
    faculties: List[Faculty]
    hours: int
    student_group: str
    fixed_hours: Optional[List[int]] = None

    @classmethod
    def create_events_from_assignments(
        cls, assignments: List[Assignment]
    ) -> List[Event]:
        events: List[Event] = []
        for assignment in assignments:
            courses = assignment.courses
            faculties = assignment.faculties
            hours = assignment.hours
            fixed_hours = assignment.fixed_hours
            weighted_hours = assignment.weighted_hours
            student_group = assignment.student_group
            if assignment.is_shared:
                for i in range(len(faculties)):
                    events.append(
                        cls(
                            courses=courses,
                            faculties=[faculties[i]],
                            hours=weighted_hours[i],
                            student_group=student_group,
                        )
                    )
            else:
                events.append(
                    cls(
                        courses=courses,
                        faculties=faculties,
                        hours=hours,
                        fixed_hours=fixed_hours,
                        student_group=student_group,
                    )
                )
        return events


def main():
    json_string = """[
    {
        "courseType": "Core",
        "isShared": false,
        "courses": [
            {
                "code": "CS101",
                "name": "Computer Science 1"
            },
            {
                "code": "CS201",
                "name": "Computer Science 2"
            }
        ],
        "faculties": [
            {
                "code": "CS",
                "name": "Computer Science",
                "occupiedHours": [1, 2, 3]
            }
        ],
        "hours": 8,
        "fixedHours": [1, 2, 3],
        "studentGroup": "A"
    },
    {
        "courseType": "Core",
        "isShared": true,
        "courses": [
            {
                "code": "MAT101",
                "name": "Mathematics 1"
            }
        ],
        "faculties": [
            {
                "code": "MATH",
                "name": "Mathematics",
                "occupiedHours": [7, 8, 9]
            },
            {
                "code": "PHY",
                "name": "Physics",
                "occupiedHours": [10, 11, 12]
            }
        ],
        "hours": 6,
        "weightedHours": [2, 4],
        "studentGroup": "B"
    },
    {
        "courseType": "Elective",
        "isShared": false,
        "courses": [
            {
                "code": "ENG101",
                "name": "English 1"
            },
            {
                "code": "ENG201",
                "name": "English 2"
            }
        ],
        "faculties": [
            {
                "code": "ENG",
                "name": "English",
                "occupiedHours": [13, 14, 15]
            },
            {
                "code": "HIS",
                "name": "History",
                "occupiedHours": [16, 17, 18]
            }
        ],
        "hours": 7,
        "fixedHours": [13, 14, 15],
        "studentGroup": "C"
    }
]"""

    json_dict = json.loads(json_string)
    json_dict = convert_keys(json_dict, "snakecase")
    assignments = [Assignment.from_json_dict(object) for object in json_dict]
    events = Event.create_events_from_assignments(assignments)
    for event in events:
        ic(type(event))


if __name__ == "__main__":
    main()
