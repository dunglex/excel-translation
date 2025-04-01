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

        # Flatten the JSON object
        flatten_data = _flatten_object(data)
        # Convert dictionary to a Pandas DataFrame
        df = pandas.DataFrame(flatten_data.items(), columns=["key", "value"])
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

        # Flatten the YAML object
        flatten_data = _flatten_object(data)
        # Convert dictionary to a Pandas DataFrame
        df = pandas.DataFrame(flatten_data.items(), columns=["key", "value"])
        # Write DataFrame to Excel file
        df.to_excel(excel_file, index=False)


def excel_to_json(excel_file, json_file, level: int = -1):
    """
    Convert Excel to JSON
    """
    # Read Excel file
    data = pandas.read_excel(excel_file, dtype=str)
    # Sort "key" column by alphabetical order
    data = data.sort_values(by=["key"], ascending=True)

    # Convert data to JSON string
    data_dict = {}
    for _, row in data.iterrows():
        key = row['key']
        value = row['value']
        if '.' in key:
            keys = key.split('.', maxsplit=-1)
            current = data_dict
            for k in keys[:-1]:
                current = current.setdefault(k, {})
            current[keys[-1]] = value
        else:
            data_dict[key] = value
    
    json_data = json.dumps(data_dict, indent=4, ensure_ascii=False)
    with open(json_file, "w", encoding="utf-8") as file:
        file.write(json_data)


def excel_to_yaml(excel_file, yaml_file):
    """
    Convert Excel to YAML
    """
    # Read Excel file
    data = pandas.read_excel(excel_file, dtype=str)
    data = data.sort_values(by=["key"], ascending=True)
    # Convert data to a dictionary
    data_dict = {}
    for _, row in data.iterrows():
        key = row['key']
        value = row['value']
        if '.' in key:
            keys = key.split('.', maxsplit=-1)
            current = data_dict
            for k in keys[:-1]:
                current = current.setdefault(k, {})
            current[keys[-1]] = value
        else:
            data_dict[key] = value

    # Convert dictionary to YAML string
    yaml_data = yaml.dump(data_dict, default_flow_style=False)
    with open(yaml_file, "w", encoding="utf-8") as file:
        file.write(yaml_data)

def _flatten_object(obj, separator='.'):
    output = {}

    def flatten(x, name='', separator=separator):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + separator, separator=separator)
        else:
            output[name[:-1]] = x
    
    flatten(obj)
    return output