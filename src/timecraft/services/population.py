import numpy as np
import json

from icecream import ic
from numpy.random import rand, randint, choice
from timecraft.services import DataHelper
from timecraft.models import Event, Assignment
from timecraft.utils import convert_keys


class Population:
    def __init__(self, data_helper):
        self.no_slots = data_helper.no_slots
        self.no_groups = data_helper.no_groups
        self.event_map = data_helper.event_map
        self.group_to_index = data_helper.group_to_index
        self.index_to_group = data_helper.index_to_group
        self.pickable_event_ids_by_group = data_helper.pickable_event_ids_by_group
        self.data_helper = data_helper

    def get_population(self, population_size=5):
        population = np.zeros(
            (population_size, self.no_groups, self.no_slots), dtype=int
        )
        for i in range(self.no_groups):
            pickable_event_ids = self.pickable_event_ids_by_group[
                self.index_to_group[i]
            ]
            if pickable_event_ids:
                population[:, i, :] = choice(
                    pickable_event_ids, size=(population_size, self.no_slots)
                )

        initial_timetable = self.get_initial_timetable()

        if initial_timetable.any():
            mask = 1 - np.minimum(1, initial_timetable)
            mask = np.expand_dims(mask, axis=0)
            population = mask * population + np.expand_dims(initial_timetable, axis=0)

        return initial_timetable, population

    def get_initial_timetable(self):
        timetable = np.zeros((self.no_groups, self.no_slots), dtype=int)
        for id, event in self.event_map.items():
            if event.fixed_slots:
                group_index = self.group_to_index[event.student_group]
                for i in event.fixed_slots:
                    timetable[group_index, i] = id
        return timetable


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
    population = Population(data_helper)
    ic(population.get_population())


if __name__ == "__main__":
    main()
