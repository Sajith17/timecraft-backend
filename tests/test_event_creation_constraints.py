import unittest
from src.timecraft.models import Faculty
from src.timecraft.event_creation.event import Class, DataHelper
from src.timecraft.event_creation.constraints import (
    HourConstraint,
    FacultyOverlapConstraint,
    ColumnRedundancyConstraint,
)

from icecream import ic


class TestConstraints(unittest.TestCase):
    def test_hour_constraint(self):
        classes = [
            Class(
                course_code="Math",
                faculties=[Faculty(code="MATH1", occupied_slots=[2, 3])],
                no_hours=3,
            ),
            Class(
                course_code="Math",
                faculties=[Faculty(code="MATH2", occupied_slots=[0, 1])],
                no_hours=3,
            ),
            Class(
                course_code="Eng",
                faculties=[Faculty(code="ENG1", occupied_slots=[0, 1])],
                no_hours=3,
            ),
            Class(
                course_code="Eng",
                faculties=[Faculty(code="ENG2", occupied_slots=[0, 1])],
                no_hours=3,
            ),
        ]
        assignment = [[0, 0, 1, 0, 1, 1]]
        fixed_slots = [0, 1, 2]
        data_helper = DataHelper(classes=classes, no_slots=0, fixed_slots=fixed_slots)
        self.assertEqual(
            HourConstraint(data_helper=data_helper).calculate_fitness_score(
                assignment=assignment
            ),
            0,
        )
        assignment = [[0, 0, 1, 0, 0, 0]]
        data_helper.fixed_slots = [0, 1, 2]
        self.assertEqual(
            HourConstraint(data_helper=data_helper).calculate_fitness_score(
                assignment=assignment
            ),
            2,
        )
        assignment = [[0, 0, 0, 0, 0, 0], [2, 2, 2, 2, 2, 2]]
        self.assertEqual(
            HourConstraint(data_helper=data_helper).calculate_fitness_score(
                assignment=assignment
            ),
            6,
        )

    def test_faculty_overlap_constraint_no_overlap(self):
        classes = [
            Class(
                course_code="Math",
                faculties=[Faculty(code="MATH1", occupied_slots=[2, 3])],
                no_hours=3,
            ),
            Class(
                course_code="Math",
                faculties=[Faculty(code="MATH3", occupied_slots=[0, 1])],
                no_hours=3,
            ),
        ]
        assignment = [[0, 0, 1, 0, 0, 1]]
        fixed_slots = [0, 1, 2]
        data_helper = DataHelper(classes=classes, no_slots=0, fixed_slots=fixed_slots)
        self.assertEqual(
            FacultyOverlapConstraint(data_helper=data_helper).calculate_fitness_score(
                assignment=assignment
            ),
            0,
        )

    def test_faculty_overlap_constraint_single_overlap(self):
        classes = [
            Class(
                course_code="Math",
                faculties=[Faculty(code="MATH1", occupied_slots=[0, 2])],
                no_hours=3,
            ),
            Class(
                course_code="Math",
                faculties=[Faculty(code="MATH3", occupied_slots=[1])],
                no_hours=3,
            ),
        ]
        assignment = [[0, 0, 1, 0, 0, 1]]
        fixed_slots = [0, 1, 2]
        data_helper = DataHelper(classes=classes, no_slots=0, fixed_slots=fixed_slots)
        self.assertEqual(
            FacultyOverlapConstraint(data_helper=data_helper).calculate_fitness_score(
                assignment=assignment
            ),
            1,
        )

    def test_faculty_overlap_constraint_multiple_overlap(self):
        classes = [
            Class(
                course_code="Math",
                faculties=[Faculty(code="MATH1", occupied_slots=[0, 2, 4])],
                no_hours=3,
            ),
            Class(
                course_code="Math",
                faculties=[Faculty(code="MATH3", occupied_slots=[1, 3, 5])],
                no_hours=3,
            ),
        ]
        assignment = [[0, 1, 0, 1, 0, 1]]
        fixed_slots = [0, 1, 2, 3, 4, 5]
        data_helper = DataHelper(classes=classes, no_slots=0, fixed_slots=fixed_slots)
        self.assertEqual(
            FacultyOverlapConstraint(data_helper=data_helper).calculate_fitness_score(
                assignment=assignment
            ),
            6,
        )

    def test_column_redundancy_constraint(self):
        classes = [
            Class(
                course_code="Math",
                faculties=[Faculty(code="MATH1", occupied_slots=[2, 3])],
                no_hours=3,
            ),
            Class(
                course_code="Math",
                faculties=[Faculty(code="MATH2", occupied_slots=[0, 1])],
                no_hours=3,
            ),
            Class(
                course_code="Eng",
                faculties=[Faculty(code="ENG1", occupied_slots=[0, 1])],
                no_hours=3,
            ),
            Class(
                course_code="Eng",
                faculties=[Faculty(code="ENG2", occupied_slots=[0, 1])],
                no_hours=3,
            ),
        ]
        assignment = [[1, 1, 1, 0, 0, 0], [2, 2, 2, 3, 3, 3]]
        fixed_slots = []
        data_helper = DataHelper(classes=classes, no_slots=0, fixed_slots=fixed_slots)
        self.assertEqual(
            ColumnRedundancyConstraint(data_helper=data_helper).calculate_fitness_score(
                assignment=assignment
            ),
            2,
        )
        assignment = [[1, 1, 1, 0, 0, 0], [3, 2, 3, 2, 3, 2]]
        self.assertEqual(
            ColumnRedundancyConstraint(data_helper=data_helper).calculate_fitness_score(
                assignment=assignment
            ),
            4,
        )
        data_helper.fixed_slots = [1, 2, 3, 4, 5, 6]
        self.assertEqual(
            ColumnRedundancyConstraint(data_helper=data_helper).calculate_fitness_score(
                assignment=assignment
            ),
            0,
        )
        data_helper.fixed_slots = [1, 2, 3]
        self.assertEqual(
            ColumnRedundancyConstraint(data_helper=data_helper).calculate_fitness_score(
                assignment=assignment
            ),
            2,
        )


if __name__ == "__main__":
    unittest.main()
