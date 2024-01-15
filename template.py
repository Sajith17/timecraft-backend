import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format="[%(asctime)s]: %(message)s:")

project_name = "timecraft"

list_of_files = [
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/utils.py",
    f"src/{project_name}/constants.py",
    f"src/{project_name}/event_creation/__init__.py",
    f"src/{project_name}/event_creation/event.py",
    f"src/{project_name}/event_creation/constraints.py",
    f"src/{project_name}/event_creation/genome.py",
    f"src/{project_name}/event_creation/fitness_calculator.py",
    f"src/{project_name}/event_creation/population.py",
    f"src/{project_name}/timetable_generation/__init__.py",
    f"src/{project_name}/timetable_generation/data_helper.py",
    f"src/{project_name}/models.py",
    f"src/{project_name}/pipeline.py",
    "requirements.txt",
    "setup.py",
    "notebook/trials.ipynb",
    "tests/test.py",
    "tests/test_event_creation_genome.py",
    "tests/test_event_creation_constraints.py",
]


for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"creating directory; {filedir} for the file {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
        logging.info(f"creating file; {filepath}")
    else:
        logging.info(f"file already exists; {filepath}")
