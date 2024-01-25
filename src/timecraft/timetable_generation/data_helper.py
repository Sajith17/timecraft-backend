import json
from timecraft.event_creation.event import Event
from timecraft.event_creation.event_creation import EventCreation
from timecraft.models import Faculty, JointCourses
from timecraft.sample_data_prep import get_data

from dataclasses import dataclass
from typing import List, Dict

from icecream import ic


@dataclass
class DataHelper:
    """
    Provide convenient access to the required helper variables during timetable generation.
    """

    no_hours: int
    no_days: int
    student_groups: List[str]
    events: List[Event]
    faculties: List[Faculty]
    _occupied_faculties_by_slots: List[List[str]] = None
    _events_by_student_group: Dict[str, List[List[int]]] = None

    @property
    def no_slots(self):
        return self.no_hours * self.no_days

    @property
    def occupied_faculty_codes_by_slots(self):
        if not self._occupied_faculties_by_slots:
            self._occupied_faculties_by_slots = [[] for _ in range(self.no_slots)]
            for faculty in self.faculties:
                if faculty.occupied_slots:
                    for occupied_slot in faculty.occupied_slots:
                        self._occupied_faculties_by_slots[occupied_slot].append(
                            faculty.code
                        )
        return self._occupied_faculties_by_slots

    @property
    def events_by_student_group(self):
        if not self._events_by_student_group:
            self._events_by_student_group = {
                student_group: [[], []] for student_group in self.student_groups
            }
            for i, event in enumerate(self.events):
                if event.fixed_slots:
                    self._events_by_student_group[event.student_group][1].append(i)
                else:
                    self._events_by_student_group[event.student_group][0].append(i)
        return self._events_by_student_group


def main():
    data_helper = DataHelper(**get_data())
    ic(data_helper.events_by_student_group)


if __name__ == "__main__":
    main()
