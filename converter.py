"""
This module contains functions to convert data between different formats.
"""
import json
import yaml
import pandas


class SingleQuotedDumper(yaml.Dumper):
    """
    Custom YAML dumper that uses single quotes for strings.
    """
    def represent_str(self, data):
        return self.represent_scalar('tag:yaml.org,2002:str', data, style="'")

SingleQuotedDumper.add_representer(str, SingleQuotedDumper.represent_str)


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
        value = str(row['value'])
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
        value = str(row['value'])
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
        if isinstance(x, dict):
            for a in x:
                flatten(x[a], str(name) + str(a) + str(separator), separator=separator)
        else:
            output[name[:-1]] = x

    flatten(obj)
    return output


def json_files_to_excel(eng_file, vi_file, excel_file, sheet_name='translation'):
    """
    Convert two JSON files to a single Excel file with two sheets
    """
    # Read JSON files
    with open(eng_file, "r", encoding="utf-8") as file:
        eng_data = json.load(file)
    with open(vi_file, "r", encoding="utf-8") as file:
        vi_data = json.load(file)

    eng_dict = _flatten_object(eng_data)
    vi_dict = _flatten_object(vi_data)

    # merge the two dictionaries, using the same key
    # the column name of value in eng_file is "eng" and in vi_file is "vi"
    merged_data = {}
    for key in set(eng_dict.keys()).union(vi_dict.keys()):
        en = str(eng_dict.get(key, ""))
        vi = str(vi_dict.get(key, ""))
        merged_data[key] = {
            "eng": en,
            "vi": vi
        }

    # Convert merged data to a DataFrame
    df = pandas.DataFrame(merged_data).T.reset_index()
    df.columns = ["key", "eng", "vi"]

    # Sort the DataFrame by the "key" column
    df = df.sort_values(by=["key"], ascending=True)

    # Write DataFrame to Excel file
    df.to_excel(excel_file, sheet_name=sheet_name, index=False)


def excel_to_json_files(excel_file, eng_file, vi_file, deep_level: int = 1):
    """
    Convert Excel file to two JSON files
    """
    # Read Excel file
    data = pandas.read_excel(excel_file, dtype=str)
    data = data.fillna('')

    # Sort "key" column by alphabetical order
    data = data.sort_values(by=["key"], ascending=True)

    # Convert data to JSON, first column is "key"
    # Second column is "eng" for eng_file
    # Third column is "vi", for vi_file
    eng_data_dict = {}
    vi_data_dict = {}
    for _, row in data.iterrows():
        key = row['key']
        eng_value = str(row['eng']) if row['eng'] is not None else ""
        vi_value = str(row['vi']) if row['eng'] is not None else ""

        if '.' in key:
            keys = key.split('.', maxsplit=deep_level)  # Extract top-level only
            
            # Populate eng_data_dict
            eng_current = eng_data_dict
            for k in keys[:-1]:
                if k not in eng_current or not isinstance(eng_current[k], dict):
                    eng_current[k] = {}  # Ensure intermediate keys are dictionaries
                eng_current = eng_current[k]
            eng_current[keys[-1]] = eng_value

            # Populate vi_data_dict
            vi_current = vi_data_dict
            for k in keys[:-1]:
                if k not in vi_current or not isinstance(vi_current[k], dict):
                    vi_current[k] = {}  # Ensure intermediate keys are dictionaries
                vi_current = vi_current[k]
            vi_current[keys[-1]] = vi_value
        else:
            eng_data_dict[key] = eng_value
            vi_data_dict[key] = vi_value

    # Convert dictionaries to JSON strings
    eng_json_data = json.dumps(eng_data_dict, indent=2, ensure_ascii=False)
    vi_json_data = json.dumps(vi_data_dict, indent=2, ensure_ascii=False)

    # Write JSON strings to files
    with open(eng_file, "w", encoding="utf-8") as file:
        file.write(eng_json_data)
    with open(vi_file, "w", encoding="utf-8") as file:
        file.write(vi_json_data)



def yaml_files_to_excel(eng_file, vi_file, excel_file, sheet_name='translation'):
    """
    Convert two YAML files to a single Excel file with two sheets
    """
    # Read YAML files
    with open(eng_file, "r", encoding="utf-8") as file:
        eng_data = yaml.safe_load(file)
    with open(vi_file, "r", encoding="utf-8") as file:
        vi_data = yaml.safe_load(file)

    eng_dict = _flatten_object(eng_data)
    vi_dict = _flatten_object(vi_data)

    # merge the two dictionaries, using the same key, the column name of value in eng_file is "eng" and in vi_file is "vi"
    merged_data = {}
    for key in set(eng_dict.keys()).union(vi_dict.keys()):
        merged_data[key] = {
            "eng": str(eng_dict.get(key, "")),
            "vi": str(vi_dict.get(key, ""))
        }

    # Convert merged data to a DataFrame
    df = pandas.DataFrame(merged_data).T.reset_index()
    df.columns = ["key", "eng", "vi"]

    # Sort the DataFrame by the "key" column
    df = df.sort_values(by=["key"], ascending=True)

    # Write DataFrame to Excel file
    df.to_excel(excel_file, sheet_name=sheet_name, index=False)


def excel_to_yaml_files(excel_file, eng_file, vi_file):
    """
    Convert Excel file to two YAML files
    """
    # Read Excel file
    data = pandas.read_excel(excel_file, dtype=str)
    data = data.fillna('')

    # Sort "key" column by alphabetical order
    data = data.sort_values(by=["key"], ascending=True)

    # Convert data to YAML, first column is "key"
    # Second column is "eng" for eng_file
    # Third column is "vi", for vi_file
    eng_data_dict = {}
    vi_data_dict = {}
    for _, row in data.iterrows():
        key = row['key']
        eng_value = str(row['eng']) if row['eng'] is not None else ""
        vi_value = str(row['vi']) if row['eng'] is not None else ""

        if '.' in key:
            keys = key.split('.', maxsplit=-1)
            
            # Populate eng_data_dict
            eng_current = eng_data_dict
            for k in keys[:-1]:
                if k not in eng_current or not isinstance(eng_current[k], dict):
                    eng_current[k] = {}  # Ensure intermediate keys are dictionaries
                eng_current = eng_current[k]
            eng_current[keys[-1]] = eng_value

            # Populate vi_data_dict
            vi_current = vi_data_dict
            for k in keys[:-1]:
                if k not in vi_current or not isinstance(vi_current[k], dict):
                    vi_current[k] = {}  # Ensure intermediate keys are dictionaries
                vi_current = vi_current[k]
            vi_current[keys[-1]] = vi_value
        else:
            eng_data_dict[key] = eng_value
            vi_data_dict[key] = vi_value

    # Convert dictionaries to YAML strings
    with open(eng_file, "w", encoding="utf-8") as file:
        yaml.dump(eng_data_dict, file, Dumper=SingleQuotedDumper, default_flow_style=False, allow_unicode=True, width=float("inf"))
    with open(vi_file, "w", encoding="utf-8") as file:
        yaml.dump(vi_data_dict, file, Dumper=SingleQuotedDumper, default_flow_style=False, allow_unicode=True, width=float("inf"))
