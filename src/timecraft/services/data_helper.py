from dataclasses import dataclass
from typing import List
from timecraft.models import Event, Assignment, create_events_from_assignments
from timecraft.utils import convert_keys
from icecream import ic

import json


class DataHelper:
    def __init__(self, no_hours: int, no_days: int, events: List[Event]) -> None:
        self.no_hours = no_hours
        self.no_days = no_days
        self.events = events

    def get_event_map(self) -> dict[int, Event]:
        event_map = {}
        for i, event in enumerate(self.events):
            event_map[i + 1] = event
        return event_map


if __name__ == "__main__":
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
    json_dict = convert_keys(json_dict, "snakecase")
    assignments = [Assignment.from_json_dict(object) for object in json_dict]
    events = create_events_from_assignments(assignments)
    data_helper = DataHelper(3, 3, events)
    ic(data_helper.get_event_map())
