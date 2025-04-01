import json
import os

from converter import json_to_excel, json_to_yaml, yaml_to_excel, yaml_to_json, excel_to_json


if __name__ == "__main__":
    sample_dict = {
        "name": "John Doe",
        "age": 30,
        "city": "New York",
        "address": {
            "street": "123 Main St",
            "zip": "10001"
        },
    }

    # create test-data directory if it doesn't exist
    if not os.path.exists("test-data"):
        os.makedirs("test-data")

    # save sample_dict as JSON
    json_data = json.dumps(sample_dict, indent=4)
    with open("test-data/sample.json", "w", encoding="utf-8") as file:
        file.write(json_data)

    # Convert JSON to YAML
    json_to_yaml("test-data/sample.json", "test-data/sample.yaml")

    # Convert JSON to EXCEL
    json_to_excel("test-data/sample.json", "test-data/sample.xlsx")

    # Convert YAML to JSON
    yaml_to_json("test-data/sample.yaml", "test-data/sample2.json")

    # Convert YAML to EXCEL
    yaml_to_excel("test-data/sample.yaml", "test-data/sample2.xlsx")

    # Convert EXCEL to JSON
    excel_to_json("test-data/sample.xlsx", "test-data/sample3.json")
