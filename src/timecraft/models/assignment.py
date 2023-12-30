from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
import json


class CourseType(Enum):
    CORE = "Core"
    ELECTIVE = "Elective"
    SHARED = "Shared"


@dataclass
class Course:
    code: str
    name: str


@dataclass
class Faculty:
    code: str
    name: str
    occupiedHours: List[int]


class Assignment:
    def __init__(
        self,
        courseType: CourseType,
        courses: List[Course],
        faculties: List[Faculty],
        hours: int,
        fixedHours: List[int],
        studentGroup: str,
        weightedHours: Optional[List[int]] = None,
    ):
        self.courseType = courseType
        self.courses = courses
        self.faculties = faculties
        self.hours = hours
        self.fixedHours = fixedHours
        self.weightedHours = weightedHours
        self.studentGroup = studentGroup

    @classmethod
    def from_json(cls, json_string):
        json_dict = json.loads(json_string)
        json_dict["courseType"] = CourseType(json_dict["courseType"])
        return cls(**json_dict)


def main():
    json_string = """{
        "courseType": "Core",
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
            },
            {
                "code": "IT",
                "name": "Information Technology",
                "occupiedHours": [4, 5, 6]
            }
        ],
        "hours": 8,
        "fixedHours": [1, 2, 3],
        "studentGroup": "A"
    }"""

    assignment = Assignment.from_json(json_string)
    print(assignment.courses, assignment.faculties, assignment.courseType)


if __name__ == "__main__":
    main()
