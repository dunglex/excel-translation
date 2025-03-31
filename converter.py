"""
This module contains functions to convert data between different formats.
"""
import json
import yaml
import pandas


def json_to_yaml(json_file, yaml_file):
    """
    Convert JSON file to YAML file
    """
    # Parse JSON string into a Python dictionary
    with open(json_file, "r", encoding="utf-8") as file:
        json_data = file.read()
        data = json.loads(json_data)
        # Convert dictionary to YAML string
        yaml_data = yaml.dump(data, default_flow_style=False)
        with open(yaml_file, "w", encoding="utf-8") as file:
            file.write(yaml_data)


def json_to_excel(json_file, excel_file):
    """
    Convert JSON file to Excel file
    """
    # Parse JSON string into a Python dictionary
    with open(json_file, "r", encoding="utf-8") as file:
        json_data = file.read()
        data = json.loads(json_data)
        # Convert dictionary to a Pandas DataFrame
        df = pandas.DataFrame(data)
        # Write DataFrame to Excel file
        df.to_excel(excel_file, index=False)


def yaml_to_json(yaml_file, json_file):
    """
    Convert YAML string to JSON string
    """
    # Parse YAML string into a Python dictionary
    with open(yaml_file, "r", encoding="utf-8") as file:
        yaml_data = file.read()
        data = yaml.safe_load(yaml_data)
        # Convert dictionary to JSON string
        json_data = json.dumps(data, indent=4)
        with open(json_file, "w", encoding="utf-8") as file:
            file.write(json_data)


def yaml_to_excel(yaml_file, excel_file):
    """
    Convert YAML string to Excel file
    """
    # Parse YAML string into a Python dictionary
    with open(yaml_file, "r", encoding="utf-8") as file:
        yaml_data = file.read()
        data = yaml.safe_load(yaml_data)
        # Convert dictionary to a Pandas DataFrame
        df = pandas.DataFrame(data)
        # Write DataFrame to Excel file
        df.to_excel(excel_file, index=False)


def excel_to_json(excel_file, json_file):
    """
    Convert Excel to JSON
    """
    # Read Excel file
    data = pandas.read_excel(excel_file)
    # Convert data to JSON string
    json_data = data.to_json(orient="records", indent=4)
    with open(json_file, "w", encoding="utf-8") as file:
        file.write(json_data)
