import json                     # Load JSON
import os                       # Join paths
import sys                      # User arguments
from zipfile import ZipFile     # Unzip .sb3

from parser import parse_json
from gui import launch_gui

# python3 -m venv venv && source venv/bin/activate
# pip install -r requirements.txt
# python3 codeOrama.py ./sb3_files/events.sb3 ./extracted
if __name__ == "__main__":
    # Check if user gave correct arguments
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <sb3_file_path> <extracted_sb3_file_path>")
        exit()
    sb3_path = sys.argv[1]
    output_dir = sys.argv[2]

    # Convert to zip and unzip
    with ZipFile(sb3_path, 'r') as zip_ref:
        zip_ref.extractall(output_dir)

    # Load JSON
    project_json = None
    with open(os.path.join(output_dir, "project.json"), 'r', encoding='utf-8') as f:
        project_json = json.load(f)

    # Parse JSON
    sprite_communication = parse_json(project_json)
    for key, value in sprite_communication.items():
        print(key)
        print(f"\t{value}")
        print()

    launch_gui(project_json, sprite_communication)
    