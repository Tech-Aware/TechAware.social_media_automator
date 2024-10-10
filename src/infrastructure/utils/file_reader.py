# src/infrastructure/utils/file_reader.py

import os


def read_prompt_file(filename):
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    file_path = os.path.join(project_root, 'resources', 'prompts', filename)

    with open(file_path, 'r') as file:
        return file.read().strip()
