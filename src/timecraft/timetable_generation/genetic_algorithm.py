from timecraft.timetable_generation.data_helper import DataHelper
from timecraft.timetable_generation.constraints import *
from timecraft.timetable_generation.genome import Genome

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
        for i in range(len(self.data_helper.student_groups)):
            if rand() < 0.85:
                p = randint(low=1, high=self.data_helper.no_slots - 1)
                offspring_a.timetable.append(
                    parent_a.timetable[i][:p] + parent_b.timetable[i][p:no_slots]
                )
                offspring_b.timetable.append(
                    parent_b.timetable[i][:p] + parent_a.timetable[i][p:no_slots]
                )
            else:
                offspring_a.timetable.append(parent_a.timetable[i].copy())
                offspring_b.timetable.append(parent_b.timetable[i].copy())
        return offspring_a, offspring_b

    def mutation(self, genome: Genome):
        events_by_student_group = self.data_helper.events_by_student_group
        available_slots_by_student_group = (
            self.data_helper.available_slots_by_student_group
        )
        for i, events, available_slots in zip(
            range(len(events_by_student_group)),
            events_by_student_group.values(),
            available_slots_by_student_group.values(),
        ):
            if rand() < 0.45:
                pickable_events, _ = events
                index = choice(available_slots)
                genome.timetable[i][index] = choice(pickable_events)
                genome.if_fitness_changed = True
        return genome

    def run_evolution(
        self,
        population_size=150,
        generation_limit=100,
        fitness_limit=1.5,
        verbose=True,
    ):
        population = self.generate_population(size=population_size)
        for i in range(generation_limit):
            population = sorted(
                population, key=lambda genome: genome.fitness_score, reverse=True
            )
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
        if verbose:
            print(f"Generation {i}, score = {population[0].fitness_score}")
        return population[0]


def main():
    data_helper = DataHelper(**get_data(verbose=False))
    constraints = [
        FacultyOverlapConstraint(data_helper=data_helper),
        FacultyWorkloadConstraint(data_helper=data_helper),
        HourConstraint(data_helper=data_helper),
        CourseFrequencyConstraint(data_helper=data_helper),
        CourseDistributionConstraint(data_helper=data_helper),
    ]
    ga = GeneticAlgorithm(data_helper=data_helper, constraints=constraints)
    winner = ga.run_evolution(
        population_size=150, generation_limit=1000, fitness_limit=2.0
    )
    ic(np.array(winner.timetable))
    ic(winner.fitness_score)
    for i, j in enumerate(data_helper.events):
        print(i, j.course_codes, j.faculty_codes)


if __name__ == "__main__":
    main()
