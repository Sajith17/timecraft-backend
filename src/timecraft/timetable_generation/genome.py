from timecraft.timetable_generation.data_helper import DataHelper
from timecraft.event_creation.constraints import Constraint
from timecraft.timetable_generation.constraints import *
from timecraft.timetable_generation.fitness_calculator import FitnessCalculator
from timecraft.sample_data_prep import get_data

import numpy as np
from numpy.random import choice
from typing import List
from icecream import ic


class Genome:
    def __init__(self, data_helper: DataHelper, constraints: List[Constraint]):
        self.data_helper = data_helper
        self.timetable = []
        self.fitness_calculator = FitnessCalculator(constraints=constraints)
        self.if_fitness_changed = False
        self._fitness_score = -1

    def initialize(self):
        for events in self.data_helper.events_by_student_group.values():
            pickable_events, _ = events
            self.timetable.append(
                [choice(pickable_events) for _ in range(self.data_helper.no_slots)]
            )
        self._apply_fixed_events()
        return self

    def _apply_fixed_events(self):
        for index, events in enumerate(
            self.data_helper.events_by_student_group.values()
        ):
            _, fixed_events = events
            for event_index in fixed_events:
                for fixed_slot in self.data_helper.events[event_index].fixed_slots:
                    self.timetable[index][fixed_slot] = event_index

    @property
    def fitness_score(self):
        if self._fitness_score == -1 or self.if_fitness_changed:
            self._fitness_score = self.fitness_calculator.calculate_score(
                timetable=self.timetable
            )
            self.if_fitness_changed = False
        return self._fitness_score


def main():
    data_helper = DataHelper(**get_data())
    constraints = [
        FacultyOverlapConstraint(data_helper=data_helper),
        FacultyWorkloadConstraint(data_helper=data_helper),
        HourConstraint(data_helper=data_helper),
        CourseFrequencyConstraint(data_helper=data_helper),
    ]
    genome = Genome(data_helper=data_helper, constraints=constraints).initialize()
    ic(genome.fitness_score)


if __name__ == "__main__":
    main()
