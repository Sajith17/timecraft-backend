import unittest
from src.timecraft.models import Faculty
from src.timecraft.event_creation.event import Class
from src.timecraft.event_creation.constraints import FacultyOverlapConstraint

from icecream import ic


class TestConstraints(unittest.TestCase):
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
        genome = [[0, 0, 1, 0, 0, 1]]
        fixed_slots = [0, 1, 2]
        self.assertEqual(
            FacultyOverlapConstraint().calculate_fitness(
                genome=genome, classes=classes, fixed_slots=fixed_slots
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
        genome = [[0, 0, 1, 0, 0, 1]]
        fixed_slots = [0, 1, 2]
        self.assertEqual(
            FacultyOverlapConstraint().calculate_fitness(
                genome=genome, classes=classes, fixed_slots=fixed_slots
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
        genome = [[0, 1, 0, 1, 0, 1]]
        fixed_slots = [0, 1, 2, 3, 4, 5]
        self.assertEqual(
            FacultyOverlapConstraint().calculate_fitness(
                genome=genome, classes=classes, fixed_slots=fixed_slots
            ),
            6,
        )


if __name__ == "__main__":
    unittest.main()