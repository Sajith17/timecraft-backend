from timecraft.event_creation.genome import Genome
from timecraft.event_creation.event import Class, DataHelper
from timecraft.event_creation.constraints import *
from timecraft.models import Course, Faculty
from typing import List

from numpy.random import choice, rand, randint
from icecream import ic


class GeneticAlgorithm:
    def __init__(self, data_helper: DataHelper, constraints: List[Constraint]):
        self.data_helper = data_helper
        self.constraints = constraints

    def generate_population(self, size: int = 10):
        return [
            Genome(
                data_helper=self.data_helper, constraints=self.constraints
            ).initialize()
            for _ in range(size)
        ]

    def selection_pair(self, population: List[List[int]]):
        fitness_array = [genome.fitness_score for genome in population]
        fitness_sum = sum(fitness_array)
        prob = [fitness / fitness_sum for fitness in fitness_array]
        a, b = choice(range(len(population)), p=prob, size=2, replace=False)
        return population[a], population[b]

    def crossover(self, parent_a: Genome, parent_b: Genome):
        offspring_a = Genome(data_helper=self.data_helper, constraints=self.constraints)
        offspring_b = Genome(data_helper=self.data_helper, constraints=self.constraints)
        no_slots = self.data_helper.no_slots
        for i in range(len(self.data_helper.classes_by_course_code)):
            if rand() < 1:
                p = randint(low=1, high=self.data_helper.no_slots - 1)
                offspring_a.assignment.append(
                    [parent_a.assignment[i][j] for j in range(0, p)]
                    + [parent_b.assignment[i][j] for j in range(p, no_slots)]
                )
                offspring_b.assignment.append(
                    [parent_b.assignment[i][j] for j in range(0, p)]
                    + [parent_a.assignment[i][j] for j in range(p, no_slots)]
                )
            else:
                offspring_a.assignment.append(parent_a.assignment[i])
                offspring_b.assignment.append(parent_b.assignment[i])
        return offspring_a, offspring_b

    def mutation(self, genome: Genome):
        classes_by_course_code = self.data_helper.classes_by_course_code
        for i, classes in zip(
            range(len(classes_by_course_code)), classes_by_course_code.values()
        ):
            if rand() < 1:
                index = randint(0, self.data_helper.no_slots)
                genome.assignment[i][index] = choice(classes)
        return genome

    def run_evolution(
        self,
        population_limit: int = 10,
        generation_limit: int = 100,
        fitness_limit: int = 1,
    ):
        pass


def main():
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
    data_helper = DataHelper(classes=classes, no_slots=no_slots)
    constraints = [
        FacultyOverlapConstraint(data_helper=data_helper),
        HourConstraint(data_helper=data_helper),
        ColumnRedundancyConstraint(data_helper=data_helper),
    ]
    ga = GeneticAlgorithm(data_helper=data_helper, constraints=constraints)
    population1 = ga.generate_population(size=10)
    # ic([[g.assignment, g.fitness_score] for g in population1])
    parent1, parent2 = ga.selection_pair(population=population1)
    offspring1, offspring2 = ga.crossover(parent1, parent2)
    # ic(parent1.assignment, parent2.assignment)
    # ic(offspring1.assignment, offspring2.assignment)
    ic(parent1.assignment)
    ic(ga.mutation(parent1).assignment)


if __name__ == "__main__":
    main()
