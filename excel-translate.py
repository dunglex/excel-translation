import argparse

from converter import json_files_to_excel, yaml_files_to_excel

def parse_args():
    """
    Parses command-line arguments for the translation tool.

    Returns:
        tuple: A tuple containing the input file path and output file path as strings.

    Command-line Arguments:
        --input (str): The path to the input files.
        --output (str): The path to the output file.
    """
    parser = argparse.ArgumentParser(description='translation tool')
    parser.add_argument('--input', type=str, required=True, help='input file path')
    parser.add_argument('--output', type=str, required=True, help='output file path')
    args = parser.parse_args()
    return  args.input, args.output


if __name__ == "__main__":
    # merge json files to excel
    json_files_to_excel("test-data/i18n/en.json", "test-data/i18n/vi.json", "test-data/i18n/translation.xlsx", "cma")

    #merge yaml files to excel
    yaml_files_to_excel("test-data/translation/en.yml", "test-data/translation/vn.yml", "test-data/translation/translation.xlsx", "erec")
