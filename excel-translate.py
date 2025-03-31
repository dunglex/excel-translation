import argparse



def parse_args():
    """
    Parses command-line arguments for the translation tool.

    Returns:
        tuple: A tuple containing the input file path and output file path as strings.

    Raises:
        ValueError: If the input or output file does not have one of the following extensions:
                    .yaml, .yml, .json, or .xlsx.

    Command-line Arguments:
        --input (str): The path to the input file. Must have an extension of .yaml, .yml, .json, or .xlsx.
        --output (str): The path to the output file. Must have an extension of .yaml, .yml, .json, or .xlsx.
    """
    parser = argparse.ArgumentParser(description='translation tool')
    parser.add_argument('--input', type=str, required=True, help='input file path')
    parser.add_argument('--output', type=str, required=True, help='output file path')
    args = parser.parse_args()
    if not args.input.endswith('.yaml') or \
        not args.input.endswith('.yml') or \
        not args.input.endswith('.json') or \
        not args.input.endswith('.xlsx') or \
        not args.output.endswith('.yaml') or \
        not args.output.endswith('.yml') or \
        not args.output.endswith('.json') or \
        not args.output.endswith('.xlsx'):
        raise ValueError("input and output file must be .yaml, .yml, .json or .xlsx")
    return  args.input, args.output


if __name__ == "__main__":
    input_file, output_file = parse_args()
    
