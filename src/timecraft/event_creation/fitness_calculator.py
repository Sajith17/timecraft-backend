from timecraft.event_creation.constraints import Constraint
from timecraft.event_creation.event import Class
from typing import List


class FitnessCalculator:
    def __init__(self, constraints: List[Constraint]):
        self.constraints = constraints

    def calculate_fitness_score(self, assignment: List[List[int]], classes: List[Class], fixed_slots: List[int])->float:
        fitness_score = 0
        fitness_score += self.scale(sum(constraint.calculate_fitness_score(assignment=assignment, classes=classes, fixed_slots=fixed_slots) for constraint in self.hard_constraints))
         
        
        
    @property
    def hard_constraints(self)->List[Constraint]:
        return [self.constraints for constraint in self.constraints if constraint.Type.value = 'hard']
    
    
    @property
    def soft_constraints(self)->List[Constraint]:
        return [self.constraints for constraint in self.constraints if constraint.Type.value = 'soft']
    
    @staticmethod
    def scale(x: int)->float:
        return 1/(1.0+x) 