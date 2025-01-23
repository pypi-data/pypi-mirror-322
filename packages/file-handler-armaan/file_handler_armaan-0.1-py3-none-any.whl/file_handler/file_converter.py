from .file_reader import read_file
from .file_writer import write_file

def convert_file(input_path, output_path):
    """Converts a file from one format to another."""
    data = read_file(input_path)
    write_file(output_path, data)
