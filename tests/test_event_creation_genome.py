import unittest
from src.timecraft.event_creation.genome import Genome
from src.timecraft.event_creation.event import Class, Event
from src.timecraft.models import JointCourses, Course, Faculty

from icecream import ic


class TestGenome(unittest.TestCase):
    def test_classes_by_course_code_single_normal_course(self):
        joint_courses = JointCourses(
            courses=[
                Course(
                    code="CS101",
                    faculties=[Faculty(code="MATH1")],
                    no_hours=3,
                    student_group="A",
                ),
            ]
        )
        genome = Genome(joint_courses=joint_courses)
        self.assertEqual(genome.classes_by_course_code, {"CS101": [0]})

    def test_classes_by_course_code_multiple_normal_courses(self):
        joint_courses = JointCourses(
            courses=[
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
        )
        genome = Genome(joint_courses=joint_courses)
        self.assertEqual(
            genome.classes_by_course_code,
            {
                "CS101": [0],
                "CS102": [1],
            },
        )

    def test_classes_by_course_code_single_shared_course(self):
        joint_courses = JointCourses(
            courses=[
                Course(
                    code="CS101",
                    faculties=[Faculty(code="MATH1"), Faculty(code="MATH2")],
                    no_hours=5,
                    student_group="A",
                    faculty_hour_split=[2, 3],
                ),
            ]
        )
        genome = Genome(joint_courses=joint_courses)
        self.assertEqual(genome.classes_by_course_code, {"CS101": [0, 1]})

    def test_classes_by_course_code_multiple_shared_courses(self):
        joint_courses = JointCourses(
            courses=[
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
        )
        genome = Genome(joint_courses=joint_courses)
        self.assertEqual(
            genome.classes_by_course_code,
            {
                "CS101": [0, 1],
                "CS102": [2, 3],
            },
        )

    def test_classes_by_course_code_normal_and_shared_courses(self):
        joint_courses = JointCourses(
            courses=[
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
        )
        genome = Genome(joint_courses=joint_courses)
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
                faculties=[Faculty(code="MATH1"), Faculty(code="Math2")],
                no_hours=3,
                student_group="A",
            ),
            Course(
                code="CS102",
                faculties=[Faculty(code="MATH3"), Faculty(code="MATH4")],
                no_hours=3,
                student_group="A",
            ),
        ]
        fixed_slot = []
        genome = Genome(courses=courses, fixed_slots=fixed_slot)
        ic(genome.initialize)


if __name__ == "__main__":
    unittest.main()
