import unittest
from src.timecraft.models import Faculty
from src.timecraft.event_creation.event import Class
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
        self.assertEqual(
            HourConstraint().calculate_fitness_score(
                assignment=assignment, classes=classes, fixed_slots=fixed_slots
            ),
            0,
        )
        assignment = [[0, 0, 1, 0, 0, 0]]
        fixed_slots = [0, 1, 2]
        self.assertEqual(
            HourConstraint().calculate_fitness_score(
                assignment=assignment, classes=classes, fixed_slots=fixed_slots
            ),
            2,
        )
        assignment = [[0, 0, 0, 0, 0, 0], [2, 2, 2, 2, 2, 2]]
        self.assertEqual(
            HourConstraint().calculate_fitness_score(
                assignment=assignment, classes=classes, fixed_slots=fixed_slots
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
        self.assertEqual(
            FacultyOverlapConstraint().calculate_fitness_score(
                assignment=assignment, classes=classes, fixed_slots=fixed_slots
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
        self.assertEqual(
            FacultyOverlapConstraint().calculate_fitness_score(
                assignment=assignment, classes=classes, fixed_slots=fixed_slots
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
        self.assertEqual(
            FacultyOverlapConstraint().calculate_fitness_score(
                assignment=assignment, classes=classes, fixed_slots=fixed_slots
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
        self.assertEqual(
            ColumnRedundancyConstraint().calculate_fitness_score(
                assignment=assignment, classes=classes, fixed_slots=fixed_slots
            ),
            2,
        )
        assignment = [[1, 1, 1, 0, 0, 0], [3, 2, 3, 2, 3, 2]]
        self.assertEqual(
            ColumnRedundancyConstraint().calculate_fitness_score(
                assignment=assignment, classes=classes, fixed_slots=fixed_slots
            ),
            4,
        )
        fixed_slots = [1, 2, 3, 4, 5, 6]
        self.assertEqual(
            ColumnRedundancyConstraint().calculate_fitness_score(
                assignment=assignment, classes=classes, fixed_slots=fixed_slots
            ),
            0,
        )
        fixed_slots = [1, 2, 3]
        self.assertEqual(
            ColumnRedundancyConstraint().calculate_fitness_score(
                assignment=assignment, classes=classes, fixed_slots=fixed_slots
            ),
            2,
        )


if __name__ == "__main__":
    unittest.main()
