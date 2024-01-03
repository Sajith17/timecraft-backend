import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format="[%(asctime)s]: %(message)s:")

project_name = "timecraft"

list_of_files = [
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/utils.py",
    f"src/{project_name}/config.py",
    f"src/{project_name}/models/__init__.py",
    f"src/{project_name}/models/assignment.py",
    f"src/{project_name}/models/event.py",
    f"src/{project_name}/services/__init__.py",
    f"src/{project_name}/services/data_helper.py",
    f"src/{project_name}/services/population.py",
    f"src/{project_name}/constants.py",
    "requirements.txt",
    "setup.py",
    "research/trials.ipynb",
    "tests/test.py",
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
