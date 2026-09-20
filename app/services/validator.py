import json
from jsonschema import validate


def validate_canonical_data(data: dict) -> bool:
    with open("schema.json", "r") as file:
        schema = json.load(file)

    validate(instance=data, schema=schema)
    return True