import os
import subprocess
import sys

def should_document(file_name):
    """
    Determine if a file should be documented based on its name.

    Args:
        file_name (str): The name of the file.

    Returns:
        bool: True if the file should be documented, False otherwise.
    """
    lower_name = file_name.lower()
    return (
        file_name.endswith('.py') and
        'example' not in lower_name and
        '_generate' not in lower_name
    )

def generate_pydoc(start_dir):
    """
    Generate pydoc documentation for Python modules in the given directory.

    Args:
        start_dir (str): The directory to start searching for Python modules.

    Returns:
        None
    """
    # Create the docs directory
    docs_dir = os.path.join(start_dir, 'docs')
    os.makedirs(docs_dir, exist_ok=True)

    # Walk through the directory
    for root, dirs, files in os.walk(start_dir):
        for file in files:
            if should_document(file):
                module_name = os.path.splitext(file)[0]
                module_path = os.path.relpath(os.path.join(root, file), start_dir)
                module_path = os.path.splitext(module_path)[0].replace(os.path.sep, '.')

                # Skip the script itself
                if module_name == os.path.splitext(os.path.basename(__file__))[0]:
                    continue

                output_file = os.path.join(docs_dir, f'{module_name}.txt')

                try:
                    # Run pydoc and capture the output
                    result = subprocess.run(
                        [sys.executable, '-m', 'pydoc', module_path],
                        capture_output=True,
                        text=True,
                        check=True
                    )

                    # Write the output to a file
                    with open(output_file, 'w') as f:
                        f.write(result.stdout)

                    print(f"Generated documentation for {module_path} in {output_file}")

                except subprocess.CalledProcessError as e:
                    print(f"Error generating documentation for {module_path}: {e}")
                except Exception as e:
                    print(f"Unexpected error for {module_path}: {e}")

if __name__ == "__main__":
    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Generate documentation
    generate_pydoc(script_dir)

    print(f"Documentation generation complete. Output is in {os.path.join(script_dir, 'docs')}")