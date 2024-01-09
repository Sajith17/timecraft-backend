from dataclasses import dataclass
from timecraft.utils import convert_keys
from typing import List, Optional
from enum import Enum
from icecream import ic

import json


@dataclass(frozen=True, slots=True)
class Faculty:
    code: str
    name: str
    occupied_slots: Optional[List[int]] = None

    @classmethod
    def from_json_dict(cls, json_dict):
        return cls(**json_dict)


@dataclass(frozen=True, slots=True)
class Course:
    code: str
    name: str
    faculties: List[Faculty]
    no_hours: int
    student_group: str
    faculty_hour_split: Optional[List[int]] = None

    @classmethod
    def from_json_dict(cls, json_dict):
        faculties = [Faculty.from_json_dict(f) for f in json_dict["faculties"]]
        json_dict["faculties"] = faculties
        return cls(**json_dict)


@dataclass(frozen=True, slots=True)
class JointCourses:
    courses: List[Course]
    fixed_slots: Optional[List[int]] = None

    @classmethod
    def from_json_dict(cls, json_dict):
        courses = [Course.from_json_dict(c) for c in json_dict["courses"]]
        json_dict["courses"] = courses
        return cls(**json_dict)

    @classmethod
    def from_json_string(cls, json_string):
        return cls.from_json_dict(json.loads(json_string))


def main():
    json_string = """{
            "courses": [
                {
                "code": "CS101",
                "name": "Computer Science 1",
                "faculties": [
                    {
                    "code": "CS",
                    "name": "Computer Science",
                    "occupiedSlots": [1, 2, 3]
                    }
                ],
                "no_hours": 8,
                "student_group": "A"
                },
                {
                "code": "CS201",
                "name": "Computer Science 2",
                "faculties": [
                    {
                    "code": "CS",
                    "name": "Computer Science"
                    }
                ],
                "no_hours": 8,
                "student_group": "B"
                }
            ],
            "fixed_slots": [1, 2, 3]
            }"""
    json_dict = json.loads(json_string)
    json_dict = convert_keys(json_dict, "snakecase")
    ic(JointCourses.from_json_dict(json_dict))


if __name__ == "__main__":
    main()
