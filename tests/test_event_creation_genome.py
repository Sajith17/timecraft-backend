import unittest
from src.timecraft.event_creation.genome import Genome
from src.timecraft.event_creation.event import Class, Event
from src.timecraft.models import JointCourses, Course, Faculty, JointCourses
from timecraft.event_creation.constraints import *

from icecream import ic


class TestGenome(unittest.TestCase):
    def test_fitness_score(self):
        courses = [
            Course(
                code="CS101",
                faculties=[Faculty(code="MATH1"), Faculty(code="MATH2")],
                no_hours=5,
                student_group="A",
            ),
            Course(
                code="CS102",
                faculties=[Faculty(code="MATH3"), Faculty(code="MATH4")],
                no_hours=5,
                student_group="A",
                faculty_hour_split=[2, 3],
            ),
        ]
        fixed_slot = []
        joint_courses = JointCourses(courses=courses, fixed_slots=fixed_slot)
        data_helper = DataHelper(joint_courses=joint_courses)
        constraints = [
            FacultyOverlapConstraint(data_helper=data_helper),
            HourConstraint(data_helper=data_helper),
            ColumnRedundancyConstraint(data_helper=data_helper),
        ]
        genome = Genome(data_helper=data_helper, constraints=constraints)
        genome.assignment = [[0, 0, 0, 0, 0], [1, 1, 2, 2, 2]]
        self.assertGreater(genome.fitness_score, 1)


if __name__ == "__main__":
    unittest.main()
