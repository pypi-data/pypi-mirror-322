import json


def json_format(data: dict):
    converted_data = {}
    for key, value in data.items():
        try:
            # Try to parse the value as JSON
            converted_data[key] = json.loads(value)
        except (json.JSONDecodeError, TypeError):
            # If it fails, keep the original value
            converted_data[key] = value
    return converted_data
