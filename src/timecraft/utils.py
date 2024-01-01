import json
import stringcase
from icecream import ic


def convert_keys(data, case_type):
    if isinstance(data, list):
        return [convert_keys(item, case_type) for item in data]
    elif isinstance(data, dict):
        converter_function = getattr(stringcase, case_type)
        return {
            converter_function(key): convert_keys(value, case_type)
            for key, value in data.items()
        }
    else:
        return data


if __name__ == "__main__":
    json_string = """{
        "courseType": "Core",
        "courses": [
            {
                "code": "CS101",
                "name": "ComputerScience 1"
            },
            {
                "code": "CS201",
                "name": "Computer Science 2"
            }
        ],
        "faculties": [
            {
                "code": "CS",
                "name": "Computer Science",
                "occupiedHours": [1, 2, 3]
            },
            {
                "code": "IT",
                "name": "Information Technology",
                "occupiedHours": [4, 5, 6]
            }
        ],
        "hours": 8,
        "fixedHours": [1, 2, 3],
        "studentGroup": "A"
    }"""
    json_dict = json.loads(json_string)
    ic(convert_keys(json_dict, "snakecase"))
    ic(convert_keys((convert_keys(json_dict, "snakecase")), "camelcase"))
