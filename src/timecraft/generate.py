from timecraft.event_creation.event_creation import EventCreation
from timecraft.timetable_generation.timetable_generation import TimetableGeneration
from timecraft.models import *

import json
from icecream import ic


def generate_timetable(data, verbose=False):
    events = EventCreation(joint_courses_list=data["joint_courses_list"]).get_events(
        verbose=verbose
    )
    timetable = (
        TimetableGeneration(
            no_hours=data["no_hours"],
            no_days=data["no_days"],
            student_groups=data["student_groups"],
            events=events,
            faculties=data["faculties"],
        )
        .generate(verbose=verbose)
        .timetable
    )
    return {"events": events, "timetable": timetable}


if __name__ == "__main__":
    data_path = r"C:\Users\sajit\OneDrive\Documents\Desktop\Pythonn\Git\timecraft-backend\src\timecraft\sample_data.json"
    with open(data_path, "r") as f:
        data = json.load(f)
    joint_courses_list = [
        JointCourses.from_json_dict(joint_courses)
        for joint_courses in data["joint_courses_list"]
    ]
    data = {
        "no_hours": data["no_hours"],
        "no_days": data["no_days"],
        "student_groups": data["student_groups"],
        "faculties": [Faculty(**f) for f in data["faculties"]],
        "joint_courses_list": joint_courses_list,
    }
    ic(generate_timetable(data, verbose=True))
