from timecraft.event_creation.event_creation import EventCreation
from timecraft.timetable_generation.timetable_generation import TimetableGeneration
from timecraft.models import *
from dataclasses import asdict
from timecraft.utils import convert_keys

import json
from icecream import ic


def generate_timetable(data, verbose=False):
    data = convert_keys(data, "snakecase")
    data = {
        "no_hours": int(data["no_hours"]),
        "no_days": int(data["no_days"]),
        "student_groups": data["student_groups"],
        "faculties": [Faculty(**f) for f in data["faculties"]],
        "joint_courses_list": [
            JointCourses.from_json_dict(joint_courses)
            for joint_courses in data["joint_courses_list"]
        ],
    }
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
    d = {
        "student_groups": data["student_groups"],
        "events": list(
            {"classes": event["classes"], "student_group": event["student_group"]}
            for event in map(asdict, events)
        ),
        "timetable": [list(map(int, l)) for l in timetable],
    }
    return convert_keys(d, "camelcase")


if __name__ == "__main__":
    data_path = r"C:\Users\sajit\OneDrive\Documents\Desktop\Pythonn\Git\timecraft-backend\src\timecraft\sample_data.json"
    with open(data_path, "r") as f:
        data = json.load(f)
    with open("sampleDataCamelCase.json", "w") as json_file:
        json.dump(convert_keys(data, "camelcase"), json_file)
    # ic(generate_timetable(data, verbose=True))
