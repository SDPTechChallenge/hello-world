
import os


def get_root_filepath(file_path: str) -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", file_path))
