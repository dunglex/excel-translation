import argparse

from converter import excel_to_json, excel_to_yaml, json_to_excel, json_to_yaml, yaml_to_excel, yaml_to_json


def parse_args():
    """
    Parses command-line arguments for the translation tool.

    Returns:
        tuple: A tuple containing the input file path and output file path as strings.

    Command-line Arguments:
        --input (str): The path to the input file. Must have an extension of .yaml, .yml, .json, or .xlsx.
        --output (str): The path to the output file. Must have an extension of .yaml, .yml, .json, or .xlsx.
    """
    parser = argparse.ArgumentParser(description='translation tool')
    parser.add_argument('--input', type=str, required=True, help='input file path')
    parser.add_argument('--output', type=str, required=True, help='output file path')
    args = parser.parse_args()
    return  args.input, args.output


if __name__ == "__main__":
    input_file, output_file = parse_args()

    if input_file.endswith('.yaml') or input_file.endswith('.yml'):
        if output_file.endswith('.json'):
            yaml_to_json(input_file, output_file)
        elif output_file.endswith('.xlsx'):
            yaml_to_excel(input_file, output_file)
    elif input_file.endswith('.json'):
        if output_file.endswith('.yaml') or output_file.endswith('.yml'):
            json_to_yaml(input_file, output_file)
        elif output_file.endswith('.xlsx'):
            json_to_excel(input_file, output_file)
    elif input_file.endswith('.xlsx'):
        if output_file.endswith('.yaml') or output_file.endswith('.yml'):
            excel_to_yaml(input_file, output_file)
        elif output_file.endswith('.json'):
            excel_to_json(input_file, output_file)
    else:
        print("Unsupported file format. Please use .yaml, .yml, .json, or .xlsx.")