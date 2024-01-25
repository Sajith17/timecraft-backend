import json
from timecraft.models import JointCourses
from timecraft.event_creation.event_creation import EventCreation
from dataclasses import asdict
from box import Box


from icecream import ic


def main():
    data_path = r"C:\Users\sajit\OneDrive\Documents\Desktop\Pythonn\Git\timecraft-backend\src\timecraft\sample_data.json"
    with open(data_path, "r") as f:
        data = json.load(f)
    joint_courses_list = [
        JointCourses.from_json_dict(joint_courses)
        for joint_courses in data["joint_courses_list"]
    ]
    events = EventCreation(joint_courses_list=joint_courses_list).get_events(
        verbose=True
    )
    event_data = {
        "no_hours": data["no_hours"],
        "no_days": data["no_hours"],
        "faculties": data["faculties"],
        "events": [asdict(event) for event in events],
    }
    with open("sample_events.json", "w") as f:
        json.dump(event_data, f)


def get_data():
    path = r"C:\Users\sajit\OneDrive\Documents\Desktop\Pythonn\Git\timecraft-backend\sample_events.json"
    with open(path, "r") as f:
        data = json.load(f)
    return Box(data)


if __name__ == "__main__":
    ic(get_data())
