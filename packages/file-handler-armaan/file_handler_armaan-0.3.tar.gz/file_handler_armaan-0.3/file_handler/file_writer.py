import json
import yaml
import csv
from pathlib import Path

def write_file(file_path, data):
    """Writes data to a file based on its extension."""
    file_path = Path(file_path)
    file_extension = file_path.suffix.lower()

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            if file_extension == '.json':
                json.dump(data, f, indent=2)
            elif file_extension in {'.yaml', '.yml'}:
                yaml.dump(data, f)
            elif file_extension == '.csv':
                if isinstance(data, list) and data and isinstance(data[0], dict):
                    writer = csv.DictWriter(f, fieldnames=data[0].keys())
                    writer.writeheader()
                    writer.writerows(data)
                else:
                    raise ValueError("CSV data must be a list of dictionaries.")
            elif file_extension == '.txt':
                if isinstance(data, list):
                    f.write("\n".join(data))
                else:
                    raise ValueError("TXT data must be a list of strings.")
            else:
                raise ValueError(f"Unsupported file format: {file_extension}")
    except Exception as e:
        raise RuntimeError(f"Error writing file {file_path}: {e}")
