from timecraft.event_creation.constraints import Constraint
from timecraft.timetable_generation.data_helper import DataHelper
from timecraft.timetable_generation.genome import Genome

from timecraft.sample_data_prep import get_data

import math
import numpy as np
from typing import List
from collections import Counter
from icecream import ic


class HourConstraint(Constraint):
    def __init__(self, data_helper: DataHelper):
        super().__init__(type=super().Type("hard"))
        self.data_helper = data_helper

    def calculate_fitness_score(self, timetable: List[List[int]]):
        fitness_score = 0
        event_freq = {}
        for i in timetable:
            for j in i:
                if j in event_freq:
                    event_freq[j] += 1
                else:
                    event_freq[j] = 1
        fitness_score = sum(
            abs(event_freq[event_index] - self.data_helper.events[event_index].no_hours)
            for event_index in event_freq
        )
        return fitness_score


class FacultyOverlapConstraint(Constraint):
    def __init__(self, data_helper: DataHelper):
        super().__init__(type=super().Type("hard"))
        self.data_helper = data_helper

    def calculate_fitness_score(self, timetable: List[List[int]]):
        fitness_score = 0
        for slot in range(self.data_helper.no_slots):
            faculty_code_list = []
            for group_index in range(len(self.data_helper.student_groups)):
                faculty_code_list.extend(
                    self.data_helper.events[timetable[group_index][slot]].faculty_codes
                )
            faculty_code_list.extend(
                self.data_helper.occupied_faculty_codes_by_slots[slot]
            )
            fitness_score += len(faculty_code_list) - len(set(faculty_code_list))
        return fitness_score


class FacultyWorkloadConstraint(Constraint):
    def __init__(self, data_helper: DataHelper):
        super().__init__(type=super().Type("hard"))
        self.data_helper = data_helper

    def calculate_fitness_score(self, timetable: List[List[int]]):
        fitness_score = 0
        no_hours = self.data_helper.no_hours
        for day in range(self.data_helper.no_days):
            faculty_code_list = []
            for slot in range(day * no_hours, (day + 1) * no_hours):
                for group_index in range(len(self.data_helper.student_groups)):
                    faculty_code_list.extend(
                        self.data_helper.events[
                            timetable[group_index][slot]
                        ].faculty_codes
                    )
                faculty_code_list.extend(
                    self.data_helper.occupied_faculty_codes_by_slots[slot]
                )
            fitness_score += sum(
                max(workload - 4, 0) for workload in Counter(faculty_code_list).values()
            )
        return fitness_score


class CourseFrequencyConstraint(Constraint):
    def __init__(self, data_helper: DataHelper):
        super().__init__(type=super().Type("soft"))
        self.data_helper = data_helper

    def calculate_fitness_score(self, timetable):
        fitness_score = 0
        no_hours = self.data_helper.no_hours
        for day in range(self.data_helper.no_days):
            for group_index in range(len(self.data_helper.student_groups)):
                course_code_list = []
                for slot in range(day * no_hours, (day + 1) * no_hours):
                    course_code_list.append(
                        self.data_helper.events[
                            timetable[group_index][slot]
                        ].course_codes[0]
                    )
                fitness_score += (
                    len(course_code_list) - len(set(course_code_list))
                ) ** 2
        return fitness_score / (
            len(self.data_helper.student_groups) * self.data_helper.no_days
        )


def main():
    data_helper = DataHelper(**get_data())
    timetable = Genome(data_helper=data_helper, constraints=None).initialize().timetable
    ic(np.array(timetable))
    # ic(
    #     HourConstraint(data_helper=data_helper).calculate_fitness_score(
    #         timetable=[[19], [11], [14]]
    #     )
    # )
    ic(
        FacultyOverlapConstraint(data_helper=data_helper).calculate_fitness_score(
            timetable=timetable
        )
    )
    # ic(
    #     FacultyWorkloadConstraint(data_helper=data_helper).calculate_fitness_score(
    #         timetable=timetable
    #     )
    # )
    # ic(
    #     CourseFrequencyConstraint(data_helper=data_helper).calculate_fitness_score(
    #         timetable=timetable
    #     )
    # )


if __name__ == "__main__":
    main()
