import json
import yaml
import csv
from pathlib import Path

def read_file(file_path):
    """Reads the content of a file based on its extension."""
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    file_extension = file_path.suffix.lower()
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            if file_extension == '.json':
                return json.load(f)
            elif file_extension in {'.yaml', '.yml'}:
                return yaml.safe_load(f)
            elif file_extension == '.csv':
                reader = csv.DictReader(f)
                return [row for row in reader]
            elif file_extension == '.txt':
                return f.read().splitlines()
            else:
                raise ValueError(f"Unsupported file format: {file_extension}")
    except Exception as e:
        raise RuntimeError(f"Error reading file {file_path}: {e}")
