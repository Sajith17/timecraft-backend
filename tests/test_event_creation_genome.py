import unittest
from src.timecraft.event_creation.genome import Genome
from src.timecraft.event_creation.event import Class, Event
from src.timecraft.models import JointCourses, Course, Faculty

from icecream import ic


class TestGenome(unittest.TestCase):
    def test_classes_by_course_code_single_normal_course(self):
        courses = [
            Course(
                code="CS101",
                faculties=[Faculty(code="MATH1")],
                no_hours=3,
                student_group="A",
            ),
        ]
        classes = Class.create_classes_from_courses(courses=courses)
        no_slots = courses[0].no_hours
        genome = Genome(classes=classes, no_slots=no_slots, fixed_slots=None)
        self.assertEqual(genome.classes_by_course_code, {"CS101": [0]})

    def test_classes_by_course_code_multiple_normal_courses(self):
        courses = [
            Course(
                code="CS101",
                faculties=[Faculty(code="MATH1")],
                no_hours=3,
                student_group="A",
            ),
            Course(
                code="CS102",
                faculties=[Faculty(code="MATH2"), Faculty(code="MATH3")],
                no_hours=3,
                student_group="A",
            ),
        ]
        classes = Class.create_classes_from_courses(courses=courses)
        no_slots = courses[0].no_hours
        genome = Genome(classes=classes, no_slots=no_slots, fixed_slots=None)
        self.assertEqual(
            genome.classes_by_course_code,
            {
                "CS101": [0],
                "CS102": [1],
            },
        )

    def test_classes_by_course_code_single_shared_course(self):
        courses = [
            Course(
                code="CS101",
                faculties=[Faculty(code="MATH1"), Faculty(code="MATH2")],
                no_hours=5,
                student_group="A",
                faculty_hour_split=[2, 3],
            ),
        ]

        classes = Class.create_classes_from_courses(courses=courses)
        no_slots = courses[0].no_hours
        genome = Genome(classes=classes, no_slots=no_slots, fixed_slots=None)
        self.assertEqual(genome.classes_by_course_code, {"CS101": [0, 1]})

    def test_classes_by_course_code_multiple_shared_courses(self):
        courses = [
            Course(
                code="CS101",
                faculties=[Faculty(code="MATH1"), Faculty(code="MATH2")],
                no_hours=5,
                student_group="A",
                faculty_hour_split=[1, 4],
            ),
            Course(
                code="CS102",
                faculties=[Faculty(code="MATH3"), Faculty(code="MATH4")],
                no_hours=5,
                student_group="A",
                faculty_hour_split=[2, 3],
            ),
        ]
        classes = Class.create_classes_from_courses(courses=courses)
        no_slots = courses[0].no_hours
        genome = Genome(classes=classes, no_slots=no_slots, fixed_slots=None)
        self.assertEqual(
            genome.classes_by_course_code,
            {
                "CS101": [0, 1],
                "CS102": [2, 3],
            },
        )

    def test_classes_by_course_code_normal_and_shared_courses(self):
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

        classes = Class.create_classes_from_courses(courses=courses)
        no_slots = courses[0].no_hours
        genome = Genome(classes=classes, no_slots=no_slots, fixed_slots=None)
        self.assertEqual(
            genome.classes_by_course_code,
            {
                "CS101": [0],
                "CS102": [1, 2],
            },
        )

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
        classes = Class.create_classes_from_courses(courses=courses)
        no_slots = courses[0].no_hours
        genome = Genome(classes=classes, no_slots=no_slots, fixed_slots=None)
        genome.assignment = [[0, 0, 0, 0, 0], [1, 1, 2, 2, 2]]
        self.assertGreater(genome.fitness_score, 1)


if __name__ == "__main__":
    unittest.main()
