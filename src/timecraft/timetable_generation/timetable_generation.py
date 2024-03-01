from genetic_algorithm import GeneticAlgorithm
from data_helper import DataHelper
from typing import List, Dict
from timecraft.event_creation.event import Event
from constraints import *
from timecraft.models import Faculty

from icecream import ic


class TimetableGeneration:
    def __init__(
        self,
        no_hours: int,
        no_days: int,
        student_groups: List[str],
        events: List[Event],
        faculties: List[Faculty],
    ):
        self.no_hours = no_hours
        self.no_days = no_days
        self.student_groups = student_groups
        self.events = events
        self.faculties = faculties

    def generate(self):
        data_helper = DataHelper(
            no_hours=self.no_hours,
            no_days=self.no_days,
            student_groups=self.student_groups,
            events=self.events,
            faculties=self.faculties,
        )
        constraints = [
            FacultyOverlapConstraint(data_helper=data_helper),
            FacultyWorkloadConstraint(data_helper=data_helper),
            HourConstraint(data_helper=data_helper),
            CourseFrequencyConstraint(data_helper=data_helper),
            CourseDistributionConstraint(data_helper=data_helper),
        ]
        genetic_algorithm = GeneticAlgorithm(
            data_helper=data_helper, constraints=constraints
        )
        timetable = genetic_algorithm.run_evolution(
            population_size=150, generation_limit=1000, fitness_limit=2.0, verbose=True
        )
        return timetable


def main():
    timetable_generation = TimetableGeneration(**get_data(verbose=False))
    timetable = timetable_generation.generate()
    ic(timetable)


if __name__ == "__main__":
    main()
