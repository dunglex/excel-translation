import json

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

    # save sample_dict as JSON
    json_data = json.dumps(sample_dict, indent=4)
    with open("sample.json", "w", encoding="utf-8") as file:
        file.write(json_data)

    # Convert JSON to YAML
    json_to_yaml("sample.json", "sample.yaml")

    # Convert JSON to EXCEL
    json_to_excel("sample.json", "sample.xlsx")

    # Convert YAML to JSON
    yaml_to_json("sample.yaml", "sample2.json")

    # Convert YAML to EXCEL
    yaml_to_excel("sample.yaml", "sample2.xlsx")
    
    # Convert EXCEL to JSON
    excel_to_json("sample.xlsx", "sample3.json")
