from timecraft.models import JointCourses, Course, Faculty
from timecraft.event_creation.event import Event, DataHelper
from timecraft.event_creation.genetic_algorithm import GeneticAlgorithm
from timecraft.event_creation.constraints import *

from icecream import ic

from typing import List, Dict, Tuple
import json


class EventCreation:
    def __init__(self, joint_courses_list: List[JointCourses]):
        self.joint_courses_list = joint_courses_list

    def get_events(self, verbose=True):
        events = []
        for joint_courses in self.joint_courses_list:
            data_helper = DataHelper(joint_courses=joint_courses)
            constraints = [
                FacultyOverlapConstraint(data_helper=data_helper),
                HourConstraint(data_helper=data_helper),
                ColumnRedundancyConstraint(data_helper=data_helper),
            ]
            genetic_algorithm = GeneticAlgorithm(
                data_helper=data_helper, constraints=constraints
            )
            genome = genetic_algorithm.run_evolution(verbose=verbose)
            events.extend(
                self._create_events_from_assignment(
                    assigment=genome.assignment, data_helper=data_helper
                )
            )
        return events

    def _create_events_from_assignment(
        self, assigment: List[List[int]], data_helper: DataHelper
    ):
        events = []
        unique_events = self._get_unique_class_columns(
            assigment=assigment, data_helper=data_helper
        )
        for k, v in unique_events.items():
            if v[0] > len(v[1]):
                events.append(
                    Event(
                        classes=[data_helper.classes[i] for i in k],
                        no_hours=v[0] - len(v[1]),
                        student_group=data_helper.student_group,
                    )
                )
            if v[1]:
                events.append(
                    Event(
                        classes=[data_helper.classes[i] for i in k],
                        no_hours=len(v[1]),
                        student_group=data_helper.student_group,
                        fixed_slots=v[1],
                    )
                )
        return events

    def _get_unique_class_columns(
        self, assigment: List[List[int]], data_helper: DataHelper
    ):
        unique_class_columns = {}
        for i in range(data_helper.no_slots):
            t = tuple(assigment[j][i] for j in range(len(assigment)))
            if t not in unique_class_columns:
                unique_class_columns[t] = [1, []]
            else:
                unique_class_columns[t][0] += 1
            if i < len(data_helper.fixed_slots):
                unique_class_columns[t][1].append(data_helper.fixed_slots[i])
        return unique_class_columns


def main():
    courses = [
        Course(
            code="CS101",
            faculties=[
                Faculty(code="MATH1", occupied_slots=[]),
                Faculty(code="MATH2", occupied_slots=[]),
            ],
            no_hours=6,
            student_group="A",
            faculty_hour_split=[3, 3],
        ),
        Course(
            code="CS102",
            faculties=[
                Faculty(code="MATH5", occupied_slots=[]),
                Faculty(code="MATH6", occupied_slots=[]),
            ],
            no_hours=6,
            student_group="A",
            faculty_hour_split=[3, 3],
        ),
    ]
    fixed_slots = [1, 2, 3, 4, 5]
    data_helper = DataHelper(
        joint_courses=JointCourses(courses=courses, fixed_slots=fixed_slots)
    )
    assignment = [[0, 0, 0, 1, 1, 1], [2, 2, 2, 3, 3, 3]]
    ec = EventCreation(None)._create_events_from_assignment(assignment, data_helper)
    ic(ec)
    joint_courses_list = [JointCourses(courses=courses, fixed_slots=fixed_slots)]
    ic(joint_courses_list[0])
    ec = EventCreation(joint_courses_list=joint_courses_list)
    events = ec.get_events(verbose=True)
    ic(events)
    # data_path = r"C:\Users\sajit\OneDrive\Documents\Desktop\Pythonn\Git\timecraft-backend\src\timecraft\sample_data.json"
    # with open(data_path, "r") as f:
    #     data = json.load(f)
    # joint_courses_list = [
    #     JointCourses.from_json_dict(joint_courses)
    #     for joint_courses in data["joint_courses_list"]
    # ]
    # event_creation = EventCreation(joint_courses_list=joint_courses_list)
    # ic(event_creation.get_events(verbose=False))


if __name__ == "__main__":
    main()
