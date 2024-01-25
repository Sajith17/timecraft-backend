from timecraft.timetable_generation.data_helper import DataHelper
from timecraft.event_creation.constraints import Constraint

from typing import List

class Genome:
    def __init__(self, data_helper: DataHelper, constraints: List[Constraint]):
        self.data_helper = data_helper
        self.constraints = constraints