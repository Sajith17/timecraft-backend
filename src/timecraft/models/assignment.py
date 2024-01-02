from dataclasses import dataclass
from timecraft.utils import convert_keys
from typing import List, Optional
from enum import Enum
from icecream import ic

import json


class CourseType(Enum):
    CORE = "Core"
    ELECTIVE = "Elective"


@dataclass(frozen=True, slots=True)
class Course:
    code: str
    name: str


@dataclass(frozen=True, slots=True)
class Faculty:
    code: str
    name: str
    occupied_hours: List[int]


@dataclass(frozen=True, slots=True)
class Assignment:
    course_type: CourseType
    courses: List[Course]
    faculties: List[Faculty]
    hours: int
    student_group: str
    is_shared: Optional[bool] = False
    fixed_hours: Optional[List[int]] = None
    weighted_hours: Optional[List[int]] = None

    @classmethod
    def from_json_dict(cls, json_dict):
        return cls(**json_dict)

    @classmethod
    def from_json_string(cls, json_string):
        return cls.from_json_dict(json.loads(json_string))


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

    json_dict = json.loads(json_string)
    json_dict = convert_keys(json_dict, "snakecase")
    ic(json_dict)


if __name__ == "__main__":
    main()
