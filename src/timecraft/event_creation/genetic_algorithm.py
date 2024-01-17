from timecraft.event_creation.genome import Genome
from timecraft.event_creation.event import Class, DataHelper
from timecraft.event_creation.constraints import *
from timecraft.models import Course, Faculty, JointCourses
from timecraft.event_creation.fitness_calculator import FitnessCalculator
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

    def selection_pair(self, population: List[Genome]):
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
            if rand() < 0.85:
                p = randint(low=1, high=self.data_helper.no_slots - 1)
                offspring_a.assignment.append(
                    parent_a.assignment[i][:p] + parent_b.assignment[i][p:no_slots]
                )
                offspring_b.assignment.append(
                    parent_b.assignment[i][:p] + parent_a.assignment[i][p:no_slots]
                )
            else:
                offspring_a.assignment.append(parent_a.assignment[i].copy())
                offspring_b.assignment.append(parent_b.assignment[i].copy())
        return offspring_a, offspring_b

    def mutation(self, genome: Genome):
        classes_by_course_code = self.data_helper.classes_by_course_code
        for i, classes in zip(
            range(len(classes_by_course_code)), classes_by_course_code.values()
        ):
            if rand() < 0.70:
                index = randint(0, self.data_helper.no_slots)
                genome.assignment[i][index] = choice(classes)
                genome.if_fitness_changed = True
                genome.fitness_calculator
        return genome

    def run_evolution(
        self,
        population_size=100,
        generation_limit=100,
        fitness_limit=1.5,
        verbose=True,
    ):
        population = self.generate_population(size=population_size)
        for i in range(generation_limit):
            population = sorted(
                population, key=lambda genome: genome.fitness_score, reverse=True
            )
            # currrent_best_score = self.fitness(population[0])
            # if currrent_best_score>self.best_score:
            #     self.best_genome=population[0]
            #     self.best_score = currrent_best_score
            if population[0].fitness_score >= fitness_limit:
                break
            if verbose:
                print(f"Generation {i}, score = {population[0].fitness_score}")
            next_generation = population[0:2]
            for _ in range(int(population_size / 2) - 1):
                parents = self.selection_pair(population)
                offspring_a, offspring_b = self.crossover(parents[0], parents[1])
                offspring_a = self.mutation(offspring_a)
                offspring_b = self.mutation(offspring_b)
                next_generation.extend([offspring_a, offspring_b])

            population = next_generation
        population = sorted(
            population, key=lambda genome: genome.fitness_score, reverse=True
        )
        print(f"Generation {i}, score = {population[0].fitness_score}")
        return population[0], i


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
    fixed_slots = [1, 2, 3]
    data_helper = DataHelper(
        joint_courses=JointCourses(courses=courses, fixed_slots=fixed_slots)
    )
    constraints = [
        FacultyOverlapConstraint(data_helper=data_helper),
        HourConstraint(data_helper=data_helper),
        ColumnRedundancyConstraint(data_helper=data_helper),
    ]
    ga = GeneticAlgorithm(data_helper=data_helper, constraints=constraints)
    winner, _ = ga.run_evolution(population_size=150, generation_limit=100)
    ic(winner.assignment)
    ic(winner._fitness_score)
    ic(winner.if_fitness_changed)
    assignment = winner.assignment
    ic(winner.fitness_calculator.calculate_score(assignment=assignment))


if __name__ == "__main__":
    main()
