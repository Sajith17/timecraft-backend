from timecraft.event_creation.genome import Genome
from timecraft.models import Course, Faculty

from icecream import ic


class Population:
    def __init__(self, genome: Genome, size: int = 10):
        self.size = size
        self._assignments = [genome.initialize() for _ in range(size)]

    def get_assignments(self):
        return self._assignments


def main():
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
    genome = Genome(courses=courses, fixed_slots=None)
    population = Population(genome=genome, size=3)
    for genome in population.get_assignments():
        ic(genome.assignment)


if __name__ == "__main__":
    main()
