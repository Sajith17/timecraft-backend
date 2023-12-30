from dataclasses import dataclass
from typing import List, Optional
from assignment import Course, Faculty, Assignment

import json


@dataclass(frozen=True, slots=True)
class Event:
    courses: List[Course]
    faculties: List[Faculty]
    hours: int
    studentGroup: str
    fixedHours: Optional[List[int]] = None


def create_events_from_assignment(assignments: List[Assignment]) -> List[Event]:
    events: List[Event] = []
    for assignment in assignments:
        courses = assignment.courses
        faculties = assignment.faculties
        hours = assignment.hours
        fixedHours = assignment.fixedHours
        weightedHours = assignment.weightedHours
        studentGroup = assignment.studentGroup
        if assignment.isShared:
            for i in range(len(faculties)):
                events.append(
                    Event(
                        courses=courses,
                        faculties=[faculties[i]],
                        hours=weightedHours[i],
                        studentGroup=studentGroup,
                    )
                )
        else:
            events.append(
                Event(
                    courses=courses,
                    faculties=faculties,
                    hours=hours,
                    fixedHours=fixedHours,
                    studentGroup=studentGroup,
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
        "fixedHours": [7, 8, 9],
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
    assignments = [Assignment.from_json(object) for object in json_dict]
    events = create_events_from_assignment(assignments)
    for event in events:
        print(event)


if __name__ == "__main__":
    main()
