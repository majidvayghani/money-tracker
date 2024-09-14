import os
import subprocess

# Path to the linter script
LINTER_PATH = "linter.py"

# Base directory to search
BASE_DIR = "../"

# Filenames to search for
TARGET_FILES = {"views.py", "models.py", "serializers.py"}


def find_files(base_dir, filenames):
    """Find files in the base directory"""
    found_files = []
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file in filenames:
                found_files.append(os.path.join(root, file))
    return found_files


def run_linter(files):
    """Run the linter on the list of files"""
    log_filename = 'linting_log.txt'
    with open(log_filename, 'w') as log_file:
        for file in files:
            try:
                print(f"Linting {file}...")
                subprocess.run(["python", LINTER_PATH, file], check=True)
                log_file.write(f"Linted: {file}\n")
            except subprocess.CalledProcessError:
                log_file.write(f"Failed to lint: {file}\n")
            except Exception as e:
                log_file.write(f"Error with {file}: {e}\n")

    print(f"Linting complete. See 'linting_log.txt' for details.")


if __name__ == "__main__":
    files = find_files(BASE_DIR, TARGET_FILES)
    if not files:
        print("No matching files found.")
    else:
        run_linter(files)
