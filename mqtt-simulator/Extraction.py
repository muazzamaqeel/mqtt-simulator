import os

def collect_python_code(root_dir, output_file='combined_code.py'):
    """
    Collects code from all Python files in the given directory and its subdirectories,
    excluding this script file. Writes the file names and total count at the top of the output.
    
    :param root_dir: The root directory to start searching for Python files.
    :param output_file: The file where combined code will be saved.
    """
    current_script = os.path.basename(__file__)
    file_names = []  # List to store names of processed files

    with open(output_file, 'w') as outfile:
        # Search for Python files and skip this script
        for dirpath, _, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename.endswith('.py') and filename != current_script and filename != output_file:
                    file_names.append(filename)
                    file_path = os.path.join(dirpath, filename)
                    with open(file_path, 'r') as infile:
                        # Write a separator with the file name
                        outfile.write(f"\n# --- Start of {filename} ---\n")
                        outfile.write(infile.read())
                        outfile.write(f"\n# --- End of {filename} ---\n\n")
        
        # Write the summary at the top of the file
        outfile.seek(0, 0)
        outfile.write("# Collected Files:\n")
        for name in file_names:
            outfile.write(f"# - {name}\n")
        outfile.write(f"# Total files collected: {len(file_names)}\n\n")
    
    print(f"All Python code has been collected into {output_file}")
    print(f"Total files collected: {len(file_names)}")

# Run the script for the current directory
collect_python_code('.')
