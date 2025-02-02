import os
import subprocess

# Get the current directory where the script is located
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define paths relative to the current directory
python_files_dir = os.path.join(current_dir, 'python_files')
js_files_dir = os.path.join(current_dir, 'scrapper')

# List of Python files
python_files = [f"python_files/{file_name}" for file_name in [
     'scrape1.py','scrape3.py', 'scrape4.py', 'scrape5.py', 'scrape6.py', 'scrape7.py', 'scrape8.py','scrape9.py']]

# JS file
js_file = os.path.join(js_files_dir, 'scrape2.js')  # Use correct filename


# Function to execute Python files
def run_python_files():
    for file in python_files:
        print(f"Running {file}")
        subprocess.run(['python', file], check=True)

# Function to execute the JS file
def run_js_file():
    print(f"Running {js_file}")
    subprocess.run(['node', js_file], check=True)

# Main execution
def main():
    run_python_files()
    run_js_file()

if __name__ == "__main__":
    main()
