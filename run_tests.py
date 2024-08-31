import os
from binexp_parser import BinOpAst

def run_tests():
    testbench_dir = 'testbench'
    for root, dirs, files in os.walk(testbench_dir):
        for file in files:
            if 'inputs' in root and ('arith_id' in root or 'mult_id' in root):
                input_file = os.path.join(root, file)
                output_file = input_file.replace('inputs', 'outputs')
                with open(input_file, 'r') as infile, open(output_file, 'r') as outfile:
                    input_data = infile.read().strip().split()
                    expected_output = outfile.read().strip()
                    print(f"Running test {file} with input data: {input_data}")
                    if not input_data:
                        print(f"Error: Input data is empty for test {file}")
                        continue
                    try:
                        ast = BinOpAst(input_data)
                        simplified_ast = ast.simplify_binops()
                        actual_output = simplified_ast.prefix_str()
                        if actual_output == expected_output:
                            print(f"Test {file} passed.")
                        else:
                            print(f"Test {file} failed. Expected {expected_output}, got {actual_output}.")
                    except Exception as e:
                        print(f"Error running test {file}: {e}")

if __name__ == "__main__":
    run_tests()
