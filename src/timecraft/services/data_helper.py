from dataclasses import dataclass
from typing import List
from timecraft.models import Event, Assignment
from timecraft.utils import convert_keys
from icecream import ic

import json


class DataHelper:
    """
    Provide convenient access to the required helper variables during timetable generation.
    """

    def __init__(
        self, no_hours: int, no_days: int, no_groups: int, events: List[Event]
    ) -> None:
        self.no_hours = no_hours
        self.no_days = no_days
        self.no_groups = no_groups
        self.no_slots = no_hours * no_days
        self.events = events
        self._event_map = None
        self._groups = None
        self._pickable_event_ids_by_group = None
        self._open_slots_by_group = None

    @property
    def event_map(self) -> dict[int, Event]:
        if self._event_map is None:
            self._event_map = {i + 1: event for i, event in enumerate(self.events)}
        return self._event_map

    @property
    def groups(self) -> list[str]:
        if self._groups is None:
            self._groups = sorted(
                list(set(event.student_group for event in self.events))
            )
        return self._groups

    @property
    def index_to_group(self) -> dict[int, str]:
        return {i: group for i, group in enumerate(self.groups)}

    @property
    def group_to_index(self) -> dict[str, int]:
        return {group: i for i, group in enumerate(self.groups)}

    @property
    def pickable_event_ids_by_group(self) -> dict[str, list[int]]:
        if self._pickable_event_ids_by_group is None:
            self._pickable_event_ids_by_group = {i: [] for i in self.groups}
            for id, event in self.event_map.items():
                group = event.student_group
                if event.fixed_slots:
                    if len(event.fixed_slots) < event.hours:
                        self._pickable_event_ids_by_group[group].append(id)
                else:
                    self._pickable_event_ids_by_group[group].append(id)
        return self._pickable_event_ids_by_group

    @property
    def open_slots_by_group(self) -> list[list[int]]:
        if self._open_slots_by_group is None:
            fixed_slots_by_group = {i: [] for i in self.groups}
            for event in self.events:
                group = event.student_group
                if event.fixed_slots:
                    fixed_slots_by_group[group] += event.fixed_slots
            self._open_slots_by_group = {
                group: list(set(range(self.no_slots)) - set(fixed_slots))
                for group, fixed_slots in fixed_slots_by_group.items()
            }
        return self._open_slots_by_group


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
                "occupiedSlots": [1, 2, 3]
            }
        ],
        "hours": 8,
        "fixedSlots": [1, 2, 3],
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
                "occupiedSlots": [7, 8, 9]
            },
            {
                "code": "PHY",
                "name": "Physics",
                "occupiedSlots": [10, 11, 12]
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
                "occupiedSlots": [13, 14, 15]
            },
            {
                "code": "HIS",
                "name": "History",
                "occupiedSlots": [16, 17, 18]
            }
        ],
        "hours": 3,
        "fixedSlots": [2, 3, 4],
        "studentGroup": "C"
    }
]"""

    json_dict = json.loads(json_string)
    json_dict = convert_keys(json_dict, "snakecase")
    assignments = [Assignment.from_json_dict(object) for object in json_dict]
    events = Event.create_events_from_assignments(assignments)
    data_helper = DataHelper(2, 3, 3, events)
    ic(data_helper.group_to_index)


if __name__ == "__main__":
    main()
