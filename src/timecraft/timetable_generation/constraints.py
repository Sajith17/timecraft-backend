from timecraft.event_creation.constraints import Constraint
from timecraft.timetable_generation.data_helper import DataHelper

from timecraft.sample_data_prep import get_data_helper

from typing import List
from collections import defaultdict

from icecream import ic


class HourConstraint(Constraint):
    def __init__(self, data_helper: DataHelper):
        super().__init__(type=super().Type("Hard"))
        self.data_helper = data_helper

    def calculate_fitness_score(self, timetable: List[List[int]]):
        fitness_score = 0
        event_freq = defaultdict()
        for i in timetable:
            for j in i:
                event_freq[j] += 1
        fitness_score = sum(
            (event_freq[event_index] - self.data_helper.events[event_index].no_hours)
            ** 2
            for event_index in event_freq
        ) / len(event_freq)
        return fitness_score


def main():
    data_helper = get_data_helper()
    ic(data_helper)


if __name__ == "__main__":
    main()
